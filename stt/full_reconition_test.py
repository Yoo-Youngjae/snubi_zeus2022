import json
import requests
import Mic
import CRS
from importlib import reload

TEST_DATA = "D:\python files\Rbiz\STT\\audio_data\\final_test_ouput.wav"

reload(Mic)
reload(CRS)

def full_test(TEST_DATA):
    print("1. STT test[10초 입력](4원어치 test)")
    print("2. exit")
    print("[15초당 4원, 15초 미만 입력도 15초로 인식 따라서 한번 test 당 4원]\n")
    
    while True:
        num = input("Input Number: ")

        if num == '1':
            print()
            Mic.record_audio(TEST_DATA) #녹음
            res_j = CRS.stt(TEST_DATA) #Speech to Text 정보 저장    
        
            print("Result:", res_j['text']) #text 결과 출력
        
        elif num == '2':
            print("Test Finished")
            break

        else:
            print("Wrong Input")

full_test(TEST_DATA)