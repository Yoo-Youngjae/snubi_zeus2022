from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from playsound import playsound
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from sensor_msgs.msg import Image
from std_msgs.msg import Int16, Int32MultiArray
from cv_bridge import CvBridge
import rospy

import mediapipe as mp



product_name = ['Blue_Bottle', 'Chocolate', 'Clock', 'Color_Nail', 'Fish', 'Pink_Bottle', 'Remover', 'Round_Bread', 'Square_Bread', 'Sweet_Potato', 'Tomato', 'Toothpaste', 'Wet_Tissue']
product_price = [3000, 1000, 3500, 1500, 4000, 3000, 2000, 3200, 3800, 4500, 4800, 2000, 2000]

total_price = 0
products = []
object_list = []
page = 0
signal = False


def main(request):
    global page
    global signal

    if request.method == 'POST': # 지금은 버튼 이벤트로 1을 받아오도록 구현
        page = int(request.POST.get("move_page"))
        print(page)
        ######## YES를 대답해서 page 값 1을 받아오면 ########
        # TTS) 벨트 위에 물건을 차례차례 올려주세요.
        # 컨베이어 벨트 작동

    if signal == True:
        page = subscribe_tester.page
        signal = False
        return render(request, 'main/main.html', {'products': products, 'total': total_price, 'page': page})
    # page = 0: facedetection 페이지 (default)
    # page = 1: Welcome 페이지
    # page = 2: detectron 페이지
    # page = 3: 총액 안내 및 장바구니 전달 페이지
    # page = 4: Good bye 페이지
    return render(request, 'main/main.html', {'products': products, 'total': total_price, 'page': page})

class SubscribeTester:
    def __init__(self):
        self.cv_bridge = CvBridge()
        detectron_topic = '/detectron_img'
        object_label_topic = '/object_labels'
        page_num_topic = '/page_num'
        _image_sub = rospy.Subscriber(detectron_topic, Image, self._rgb_callback)
        _image_sub2 = rospy.Subscriber(object_label_topic, Int32MultiArray, self._object_label_callback)
        _page_num_sub = rospy.Subscriber(page_num_topic, Int16, self._page_num_callback)

    def _rgb_callback(self, img_msg):
        self.cv_image = self.cv_bridge.imgmsg_to_cv2(img_msg, 'passthrough')
        # cv2.imshow('detecron_img', self.cv_image)
        # cv2.waitKey(1)

    # @api_view(['GET', 'POST', ])
    def _page_num_callback(self, data):
        global signal
        self.page = int(data.data)
        print('page', self.page)

    def _object_label_callback(self, data):
        self.object_label_list = list(data.data)

        ##### if len(object_label_list) == 0 인 상태로 10초 지속 #####
        # TTS) 더 이상 구매하실 물건이 없나요?
        # STT) yes 받아오기
        # 결제 안내 및 장바구니 전달 화면으로 넘어감
        # page = 2
        #############################################################

        for i in self.object_label_list:
            if i not in object_list:
                object_list.append(i)
                products.append([product_name[i], 1, product_price[i], product_price[i]])
                playsound("/home/snubi/PycharmProjects/snubi_zeus2022/zeusweb-master/beep.mp3")
                global total_price
                total_price += product_price[i]

                print(products)


# detectron camera
class DetectronVideoCamera(object):
    def __init__(self):
        self.frame = subscribe_tester.cv_image
        threading.Thread(target=self.update, args=()).start()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            self.frame = subscribe_tester.cv_image

class FaceVideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(2)
        (self.grabbed, self.frame) = self.video.read()
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=1)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            imgRGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            results = self.faceMesh.process(imgRGB)
            if results.multi_face_landmarks:
                for faceLms in results.multi_face_landmarks:
                    self.mpDraw.draw_landmarks(self.frame, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)
                    for id, lm in enumerate(faceLms.landmark):
                        ih, iw, ic = self.frame.shape
                        x, y = int(lm.x * iw), int(lm.y * ih)
                        #print(id, x, y)

            #cv2.imshow("Image", img)
            #cv2.waitKey(1)


def detectron_gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def face_gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def camera(request):
    try:
        cam = DetectronVideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

@gzip.gzip_page
def face(request):
    try:
        facecam = FaceVideoCamera()
        return StreamingHttpResponse(gen(facecam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

subscribe_tester = SubscribeTester()
rospy.init_node('ui_image_ros_subscriber')