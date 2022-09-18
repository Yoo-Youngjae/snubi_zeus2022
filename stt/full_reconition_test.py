import json
import requests
import Record_Audio
import CRS
from playsound import playsound
from importlib import reload

TEST_DATA = "/home/snubi/PycharmProjects/snubi_zeus2022/stt/audio_data/test_ouput.wav"

reload(Mic)
reload(CRS)

def full_test(TEST_DATA):
    print("1. STT test[10초 입력](4원어치 test)")
    print("2. exit")
    print("3. 장바구니 full scenario test")
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

        elif num == '3':
            playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/안녕하세요+준오님_+BI+마트에+오신걸+환영합니다_+저는+결제를+도와드릴+누비입니다_.mp3")
            playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/셀프+계산대에+상품을+올려놓으시면%2C+결제를+도와드리겠습니다_+.mp3")
            playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/계산+목록을+확인해주시면+결제를+진행해드리겠습니다_.mp3")
            playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/결제를+진행하시겠습니까_.mp3")

            #예 아니요 마이크 입력
            print()
            Mic.record_audio(TEST_DATA)  # 녹음
            res_j = CRS.stt(TEST_DATA)  # Speech to Text 정보 저장

            print("Result:", res_j['text'])  # text 결과 출력

            pos_list = ["예", "네", "그래", "응", "해줘"]

            if res_j['text'] in pos_list:
                playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/계산+및+포인트+적립이+완료+되었습니다_.mp3")
                playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/장바구니+챙겨+가시기+바랍니다_+.mp3")
                playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/좋은+하루+되세요!.mp3")
            else:
                playsound("/home/snubi/PycharmProjects/snubi_zeus2022/stt/tts_audio/장바구니에서+상품을+다시+한번+확인해주시기+바랍니다_.mp3")

        else:
            print("Wrong Input")

full_test(TEST_DATA)