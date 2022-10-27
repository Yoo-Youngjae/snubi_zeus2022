import serial
from vision_module.vision_controller import DetectronController
import cv2
from std_msgs.msg import Int16, Int32MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rospy
from robot_global_variable import *

class VisionAgent:
    def __init__(self):
        self.cv_bridge = CvBridge()
        self.detectron_controller = DetectronController()
        self.coord_list_pub = rospy.Publisher('/coord_list', Int32MultiArray, queue_size=10)

        # for connect opencv camera
        index = 0
        arr = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
        print('camera id lists', arr)
        camera_idx = DETECTRON_CAMERA_ID
        capture = cv2.VideoCapture(camera_idx)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture = capture
        # for conveyor belt
        self.belt_switch = serial.Serial(BELT_USB_PORT, 9600)
        self.belt_sub = rospy.Subscriber('/belt_switch', Int16, self.belt_callback)
        self.object_labels_pub = rospy.Publisher('/object_labels', Int32MultiArray, queue_size=10)
        self.detectron_pub = rospy.Publisher('/detectron_img', Image, queue_size=1)
        self.belt_activate = False

    def belt_callback(self, data):
        if data.data == 1:
            self.belt_activate = True
        else:
            self.belt_activate = False
        self.belt_on_off(data.data)

    def belt_on_off(self, on_off):
        if on_off == 1: # on
            if self.belt_switch.readable() and self.belt_activate:
                self.belt_switch.write('1'.encode('utf-8'))
        else:           # off
            if self.belt_switch.readable():
                self.belt_switch.write('0'.encode('utf-8'))




if __name__ == '__main__':
    rospy.init_node('snubi_vision_agent')
    vision_agent = VisionAgent()

    while not rospy.is_shutdown():
        ret, image = vision_agent.capture.read()
        center_coordinate_list, img, object_label_list = vision_agent.detectron_controller.get_object_center_coordnates(image, show_debug=True)

        # publish center coord list
        coord_list_msg = Int32MultiArray()
        coord_list_msg.data = [i for coord in center_coordinate_list for i in coord]
        object_labels_msg = Int32MultiArray()
        object_labels_msg.data = object_label_list

        vision_agent.coord_list_pub.publish(coord_list_msg)
        vision_agent.object_labels_pub.publish(object_labels_msg)

        # cv2.imshow("Detectron", img)
        # cv2.waitKey(1)
        detectron_img_msg = vision_agent.cv_bridge.cv2_to_imgmsg(img)
        vision_agent.detectron_pub.publish(detectron_img_msg)

        # exception handling
        if len(center_coordinate_list) > 0: # some object detected
            print(center_coordinate_list[0])
            # # todo : delete
            # test_mode = True
            # if test_mode:
            #     continue
            #####################
            if center_coordinate_list[0][0] > 1000: # [stop] wait for robot picking
                vision_agent.belt_on_off(0)
            else:
                vision_agent.belt_on_off(1)





