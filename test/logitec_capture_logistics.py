import argparse
import cv2
from playsound import playsound
import threading

def play_ding() :
    playsound("./ding.mp3")

parser = argparse.ArgumentParser(description='snubi capture')
parser.add_argument('--dir', type=str, default='logistics_black_bg/',
                    help='saved directory path')
args = parser.parse_args()

i = 20
index = 0
arr = []
while i >0:
    cap = cv2.VideoCapture(index)
    if cap.read()[0]:
        arr.append(index)
        cap.release()
    index +=1
    i -= 1
print(arr)

capture = cv2.VideoCapture(0)

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

start_idx = int(input('start_idx : '))
while True:
    ret, image = capture.read()
    cv2.imshow("Image", image)
    key = cv2.waitKey(1)
    if key == 115 or key == 13: # 's' or Enter
        print('saved', start_idx)
        cv2.imwrite(args.dir+str(start_idx)+'.png', image)
        start_idx += 1
        sound = threading.Thread(target=play_ding)
        sound.start()