
import argparse
import cv2
from playsound import playsound
import threading

def play_ding() :
    playsound("./ding.mp3")


parser = argparse.ArgumentParser(description='snubi capture')
parser.add_argument('--dir', type=str, default='data/',
                    help='saved directory path')
args = parser.parse_args()

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
fps = capture.get(cv2.CAP_PROP_FPS)
name = input('video name : ')
name = name + '.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(name, fourcc, 15, (1280, 720))

while True:
    ret, image = capture.read()
    cv2.imshow("Image", image)
    key = cv2.waitKey(1)
    if key == 115 or key == 13: # 's' or Enter
        print('start')
        sound = threading.Thread(target=play_ding)
        sound.start()
        while True:
            ret, image = capture.read()
            cv2.imshow("Image", image)
            key = cv2.waitKey(1)
            out.write(image)
            if key == 115 or key == 13:  # 's' or Enter
                print('saved')
                sound = threading.Thread(target=play_ding)
                sound.start()
                break

    if key == 27: # esc를 누르면 종료
        print('STOP')
        break
