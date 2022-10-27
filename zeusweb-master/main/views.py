from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse, HttpResponseRedirect
import cv2
import threading
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from playsound import playsound
from sensor_msgs.msg import Image
from std_msgs.msg import Int16, Int32MultiArray
from cv_bridge import CvBridge
import rospy
import time
import mediapipe as mp
product_info = [['아몬드브리즈 오리지널 190ml', 800, '800'],
                ['당근 1입(봉)', 2480, '2,480'],
                ['아동용 시계인형', 2000, '2,000'],
                ['[남양]초코에몽 250ml', 1000, '1,000'],
                ['촉촉란(2구)', 1500, '1,500'],
                ['[냉장]노르웨이 간고등어(특,400g)', 5980, '5,980'],
                ['방울토마토씨앗 흙 화분세트', 1000, '1,000'],
                ['[밀크앤허니]모닝빵', 1000, '1,000'],
                ['도브 뷰티바(비누) 100g', 1530, '1,530'],
                ['[스카치브라이트]올인원수세미', 1000, '1,000'],
                ['[삼립]토스트를 위해 태어난 식빵', 2400, '2,400'],
                ['[서울우유]딸기우유 200ml', 880, '880'],
                ['호박 고구마 1입(봉)', 500, '500'],
                ['[오설록]삼다꿀배티(20개입)', 9500, '9,500'],
                ['대추방울 토마토 200g', 2900, '2,900'],
                ['[깨끗한나라]물티슈(100매)', 500, '500']]

total_price = 0
total_price_str = '0'
products = []
object_list = []
page = 1
user = 0 # default = 0(비회원)
MILK_CLASS_NUM = 11

def main(request):
    global page, total_price, total_price_str, products, object_list, user
    if request.method == 'POST': # 지금은 버튼 이벤트로 1을 받아오도록 구현
        if request.POST.get("move_page") != None: # python request test용
            # User 정보 받아오는거 구현
            user = subscribe_tester.user_id
            page = int(request.POST.get("move_page"))
            print('User_ID: ', user)
            print('Python request: ', page)
            if page == 1:
                # 초기화
                subscribe_tester.item_dict = {i: 0 for i in range(19)}
                subscribe_tester.item_prev_list = []
                user = 0
                total_price = 0
                total_price_str = '0'
                products = []
                object_list = []

    return render(request, 'main/main.html', {'products': products, 'total': total_price_str, 'page': page, 'user': user})

def play_beep(idx):
    print('object_len', idx)
    playsound("/home/snubi/PycharmProjects/snubi_zeus2022/zeusweb-master/beep.mp3")


class SubscribeTester:
    def __init__(self):
        rospy.init_node('ui_image_ros_subscriber')
        self.cv_bridge = CvBridge()
        detectron_topic = '/detectron_img'
        face_topic = '/face_img'
        object_label_topic = '/object_labels'
        user_id_topic = '/user_id'
        self.user_id = 0
        self.item_dict = {i:0 for i in range(19)}
        self.item_prev_list = []
        _image_sub1 = rospy.Subscriber(detectron_topic, Image, self._rgb_callback)
        _image_sub2 = rospy.Subscriber(face_topic, Image, self._face_callback)
        _image_sub3 = rospy.Subscriber(object_label_topic, Int32MultiArray, self._object_label_callback)
        _user_id_topic_sub = rospy.Subscriber(user_id_topic, Int16, self._user_id_topic_callback)

    def _rgb_callback(self, img_msg):
        self.cv_image = self.cv_bridge.imgmsg_to_cv2(img_msg, 'passthrough')
        # cv2.imshow('detecron_img', self.cv_image)
        # cv2.waitKey(1)

    def _face_callback(self, img_msg):
        self.face_image = self.cv_bridge.imgmsg_to_cv2(img_msg, 'passthrough')

    # @api_view(['GET', 'POST', ])
    def _user_id_topic_callback(self, data):
        self.user_id = int(data.data)
        print('user_id', self.user_id)

    def _object_label_callback(self, data):
        self.object_label_list = list(data.data)
        global page
        count_threshold = 12
        if page == 3:
            # 인식된 물체 리스트에서
            for i in self.object_label_list: # 이번에 나온 물체들에 대해
                if i not in object_list:
                    if self.item_dict[i] >= 1 and i in self.item_prev_list: # existing in prev frame
                        self.item_dict[i] += 1
                        if self.item_dict[i] >= count_threshold and i not in object_list:
                            # ui 에 item 추가
                            object_list.append(i)
                            products.append([product_info[i][0], 1, product_info[i][2], i])
                            #products.append([product_name[i], 1, product_price[i], i])
                            t = threading.Thread(target=play_beep, args=(len(object_list),))
                            t.start()
                            # playsound("/home/snubi/PycharmProjects/snubi_zeus2022/zeusweb-master/beep.mp3")
                            if i == MILK_CLASS_NUM:
                                continue
                            global total_price, total_price_str
                            total_price += product_info[i][1]
                            total_price_str = str(total_price)
                            if len(total_price_str) >= 4:
                                total_price_str = str(total_price)[:-3]+','+str(total_price)[-3:]
                            print(products)

                    elif i not in self.item_prev_list and self.item_dict[i] == 0: # first appear
                        self.item_dict[i] = 1

            # 이번에 안나오고, 걸러야 하는 애들
            for j in self.item_prev_list:
                if j not in self.object_label_list:
                    self.item_dict[j] = 0
            # update item_prev_list
            self.item_prev_list = self.object_label_list



subscribe_tester = SubscribeTester()


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
            time.sleep(0.1)

class FaceVideoCamera(object):

    def __init__(self):
        self.frame = subscribe_tester.face_image
        threading.Thread(target=self.update, args=()).start()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            self.frame = subscribe_tester.face_image
            time.sleep(0.1)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.1)


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

