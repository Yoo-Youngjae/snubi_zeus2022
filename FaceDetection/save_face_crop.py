import cv2
import mediapipe as mp
import face_cropper
from PIL import Image
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

foreground_pil = Image.open('man_icon.png') #.convert("RGBA")
foreground_pil = foreground_pil.resize((600, 600))
data = np.array(foreground_pil)   # "data" is a height x width x 4 numpy array
red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

brown_areas = (red == 62) & (blue == 62) & (green == 62)
data[..., :-1][brown_areas.T] = (0, 0, 200) # Transpose back needed
foreground_pil = Image.fromarray(data)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    faces = fc.get_faces(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, #FACEMESH_CONTOURS, FACEMESH_TESSELATION
                                  drawSpec,drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                ih, iw, ic = img.shape
                x,y = int(lm.x*iw), int(lm.y*ih)
                # x,y 크롭하세요!

    # cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
    #             3, (255, 0, 0), 3)

    background_pil = Image.fromarray(img).convert("RGBA")

    width = (background_pil.width - foreground_pil.width) // 2
    height = (background_pil.height - foreground_pil.height) // 2 + 100

    background_pil.paste(foreground_pil, (width, height), foreground_pil)
    final_np = np.array(background_pil)
    cv2.imshow("Image", final_np)

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
            cv2.imwrite(f'user_face_database/{idx}.jpg', biggest_cropped_face)
            idx += 1
    except:
        print("No face!")
    #################################

    cv2.waitKey(1)

    if cv2.pollKey() != -1:  # User pressed key
        cap.release()
        cv2.destroyAllWindows()
        break
