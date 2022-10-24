import cv2
from sensor_msgs.msg import Image
import mediapipe as mp
from cv_bridge import CvBridge
import rospy
from robot_global_variable import *
from FaceDetection.face_cropper import FaceCropper
import numpy as np
from PIL import Image as PILImage

class FaceAgent:
    def __init__(self):
        self.cv_bridge = CvBridge()
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=1)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
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
        camera_idx = FACE_CAMERA_ID
        capture = cv2.VideoCapture(camera_idx)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture = capture
        self.face_pub = rospy.Publisher('/face_img', Image, queue_size=1)
        self.face_crop_pub = rospy.Publisher('/face_crop_img', Image, queue_size=1)
        self.face_cropper = FaceCropper()

        foreground_pil = PILImage.open('/home/snubi/PycharmProjects/snubi_zeus2022/FaceDetection/man_icon.png')
        foreground_pil = foreground_pil.resize((600, 600))
        data = np.array(foreground_pil)  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        brown_areas = (red == 62) & (blue == 62) & (green == 62)
        data[..., :-1][brown_areas.T] = (0, 0, 200)  # Transpose back needed
        self.foreground_pil = PILImage.fromarray(data)


if __name__ == '__main__':
    rospy.init_node('face_draw_agent')
    face_agent = FaceAgent()

    while not rospy.is_shutdown():
        ret, img = face_agent.capture.read()
        img = cv2.flip(img, 1)

        origin_img = img.copy()
        imgRGB = cv2.cvtColor(origin_img, cv2.COLOR_BGR2RGB)
        results = face_agent.faceMesh.process(imgRGB)
        faces = face_agent.face_cropper.get_faces(imgRGB)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                face_agent.mpDraw.draw_landmarks(origin_img, faceLms, face_agent.mpFaceMesh.FACEMESH_CONTOURS,
                                      face_agent.drawSpec, face_agent.drawSpec)

        background_pil = PILImage.fromarray(origin_img).convert("RGBA")

        width = (background_pil.width - face_agent.foreground_pil.width) // 2
        height = (background_pil.height - face_agent.foreground_pil.height) // 2 + 50

        background_pil.paste(face_agent.foreground_pil, (width, height), face_agent.foreground_pil)
        composited_img = np.array(background_pil)
        face_img_msg = face_agent.cv_bridge.cv2_to_imgmsg(composited_img)
        face_agent.face_pub.publish(face_img_msg)

        cropped_face_shape = []
        for face_rgb in faces:
            cropped_face_shape.append(face_rgb.shape)
        try:
            biggest_face_idx = cropped_face_shape.index(max(cropped_face_shape))
            cropped_face_img = cv2.cvtColor(faces[biggest_face_idx], cv2.COLOR_RGB2BGR)
            cropped_face_img_msg = face_agent.cv_bridge.cv2_to_imgmsg(cropped_face_img)
            face_agent.face_crop_pub.publish(cropped_face_img_msg)
            print('detected')
            # cv2.imshow('Cropped Face', cropped_face_img)
            # cv2.waitKey(1)
        except:
            print("No face!")





