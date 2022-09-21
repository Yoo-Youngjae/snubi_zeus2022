import serial
from vision_module.vision_controller import DetectronController
import cv2
from std_msgs.msg import Int16, Int32MultiArray
import rospy

class VisionAgent:
    def __init__(self):
        camera_idx = 0
        self.detectron_controller = DetectronController()
        self.coord_list_pub = rospy.Publisher('/coord_list', Int32MultiArray, queue_size=10)

        # for connect opencv camera
        index = 0
        arr = []
        for i in range(5):
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
        print('camera id lists', arr)

        capture = cv2.VideoCapture(camera_idx)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture = capture
        # for conveyor belt
        self.belt_switch = serial.Serial('/dev/ttyUSB0', 9600)
        self.belt_sub = rospy.Subscriber('/belt_switch', Int16, self.belt_callback)
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
        center_coordinate_list, img = vision_agent.detectron_controller.get_object_center_coordnates(image, show_debug=True)

        # publish center coord list
        coord_list_msg = Int32MultiArray()
        coord_list_msg.data = [i for coord in center_coordinate_list for i in coord]
        vision_agent.coord_list_pub.publish(coord_list_msg)
        cv2.imshow("Detectron", img)
        cv2.waitKey(1)

        # exception handling
        if len(center_coordinate_list) > 0: # some object detected
            print(center_coordinate_list[0])
            if center_coordinate_list[0][0] < 230: # wait for robot picking
                vision_agent.belt_on_off(0)
            else:
                vision_agent.belt_on_off(1)





