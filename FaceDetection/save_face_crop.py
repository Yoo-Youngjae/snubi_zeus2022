import cv2
import mediapipe as mp
import face_cropper
import numpy as np

idx = int(input('input new user id : '))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

fc = face_cropper.FaceCropper()

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    faces = fc.get_faces(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, #FACEMESH_CONTOURS, FACEMESH_TESSELATION
                                  drawSpec,drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                #print(lm)
                ih, iw, ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                # x,y 크롭하세요!
                #print(x, y)

    # cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
    #             3, (255, 0, 0), 3)
    cv2.imshow("Image", img)

    ################################# 추가
    cropped_face_shape = []
    for face_rgb in faces:
        cropped_face_shape.append(face_rgb.shape)
    try:
        biggest_face_idx = cropped_face_shape.index(max(cropped_face_shape))
        biggest_cropped_face = cv2.cvtColor(faces[biggest_face_idx], cv2.COLOR_RGB2BGR)
        cv2.imshow('Cropped Face', biggest_cropped_face)
        key = cv2.waitKey(1)
        print(biggest_cropped_face.shape)
        if key == 115 or key == 13 and \
            (biggest_cropped_face.shape[0] > 200 and biggest_cropped_face.shape[1] > 200):
            print("saved",idx, 'user')
            cv2.imwrite(f'/home/snubi/PycharmProjects/snubi_zeus2022/FaceDetection/user_face_database/{idx}.jpg', biggest_cropped_face)
            idx += 1
    except:
        print("No face!")
    #################################

    cv2.waitKey(1)

    if cv2.pollKey() != -1:  # User pressed key
        cap.release()
        cv2.destroyAllWindows()
        break
