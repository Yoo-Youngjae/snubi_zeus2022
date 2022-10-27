import socket
import rospy
from PIL import Image as PILImage
from sensor_msgs.msg import Image
from std_msgs.msg import Int16, Int32MultiArray
from STT.SpeechRecognition import STTController
from cv_bridge import CvBridge
import cv2
import requests
from FaceDetection.face_id import FaceId
class Agent:
    def __init__(self):
        rospy.init_node('snubi_main_agent')
        # for connect robot
        ip_addr = '192.168.0.23'
        port = 5000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket() 소켓서버 생성
        self.client_socket.connect((ip_addr, port))  # address에 있는 원격 소켓에 연결

        # init needed
        self.face_crop_img = None
        self.exist_egg = False

        self.bridge = CvBridge()
        self.belt_pub = rospy.Publisher('/belt_switch', Int16, queue_size=2)
        self.user_id_pub = rospy.Publisher('/user_id', Int16, queue_size=2)
        self.object_coord_sub = rospy.Subscriber('/coord_list', Int32MultiArray, self.coord_list_callback)
        _image_sub = rospy.Subscriber('/face_crop_img', Image, self._face_crop_callback)
        self.stt_controller = STTController()
        self.face_id_controller = FaceId()




    def __del__(self):
        self.client_socket.close() # 소켓통신 종료
    def coord_list_callback(self, data):
        self.object_coord_list = data.data
        # print(self.object_coord_list)
    def _face_crop_callback(self, img_msg):
        self.face_crop_img = self.bridge.imgmsg_to_cv2(img_msg, "passthrough")
    def send(self, data):
        data_encoded = data.encode()  # 문자열 -> byte code 변환
        self.client_socket.sendall(data_encoded)  # client socket으로 data 송신
        data = self.client_socket.recv(1024)
        return data.decode()

    def movej(self, joints, rel=False):
        if rel is True:
            msg = 'movej_rel '
            msg += ','.join(str(j) for j in joints)
            self.send(msg)
        else:
            msg = 'movej_abs '
            msg += ','.join(str(j) for j in joints)
            self.send(msg)

    def movel(self, tcp, rel=True):
        if rel is True:
            msg = 'movel_rel '
            msg += ','.join(str(j) for j in tcp)
            self.send(msg)
        else:
            msg = 'movel_abs '
            msg += ','.join(str(j) for j in tcp)
            self.send(msg)

    def getl(self):
        pos = self.send('getl ')

        # return [int(i) for i in pos.split(',')]

    def getj(self):
        pos = self.send('getj ')

        # return [int(i) for i in pos.split(',')]

    def open_gripper(self):
        self.send('open_gripper')

    def close_gripper(self):
        self.send('close_gripper')

    def motionparam_up(self):
        self.send('motionparam_up')

    def motionparam_down(self):
        self.send('motionparam_down')

    def belt_on(self):
        self.belt_pub.publish(1)

    def belt_off(self):
        self.belt_pub.publish(0)

    def get_object_coordnates_by_vision_agent(self):
        return self.object_coord_list

    def ui_page_go(self, num):
        URL = 'http://localhost:8000'
        data = {'move_page': str(num)}
        res = requests.post(URL, data=data)

    def user_id_go(self, user_id):
        self.user_id_pub.publish(int(user_id))

    def detect_face_id(self):
        face_crop_img = self.face_crop_img
        if face_crop_img is None:
            return -1
        # if face_crop_img.shape[0] < 200 or face_crop_img.shape[1] < 200:
        #     return -1
        face_croped_pil_img = PILImage.fromarray(face_crop_img)
        checked_id, user_name = self.face_id_controller.check_id(face_croped_pil_img)
        print('detect user :', user_name)
        user_id = checked_id + 1
        return user_id

    def init_variable(self):
        self.face_crop_img = None
        self.exist_egg = None

