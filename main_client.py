#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

# add jokim
import Record_Audio
import Speech_Recognition
from Text_to_Speech import *
from importlib import reload

# global variable
home_pos = [68, -9, -102, 0, -69, 69]
place_pos = [-26, -8, -94, 0, -78, -25]

INPUT_AUDIO = "/home/snubi/PycharmProjects/snubi_zeus2022/stt/audio_data/input_audio.wav"
basket_pos1 = [21, -2, 143, -86, -139, 176]
basket_pos2 = [47, 33, 152, -102, -127, 116]
# basket_pos1 = [33, -33, 137, -54, -117, 34]
# basket_pos2 = [19, 27, 127, -103, -139, 155]

def main_yjyoo(agent):
    # 1. go home posision
    agent.movej(home_pos, rel=False)
    # 2. detection object and get distance
    xyz = [-100, 0, -200]
    xyz += [0, 0, 0] # for rx,ry,rz
    # 3. go to the object
    agent.movel(xyz)
    z_offset = 10
    agent.movel([0, 0,-z_offset , 0, 0, 0])
    # 4. grasp
    agent.close_gripper()
    # 5. go to place position
    agent.movej(place_pos, rel=False)
    # 6. go to empty place
    agent.movel([0, 0, -200, 0, 0, 0])
    # 7. release the gripper
    agent.open_gripper()
    # 8. back to the place position
    agent.movej(place_pos, rel=False)

    agent.movej(home_pos, rel=False)



def main_jokim(agent):
    print("Start shopping")

    agent.movej(home_pos)

    Speak_Secnario('1')
    Speak_Secnario('4')
    Speak_Secnario('5_2')

    # 예 아니요 마이크 입력
    Record_Audio.start(INPUT_AUDIO)
    stt = Speech_Recognition.stt(INPUT_AUDIO)

    print("Result:", stt['text'])  # text 결과 출력

    pos_list = ["예", "네", "그래", "응", "해줘", "진행해줘"]

    if stt['text'] in pos_list:
        Speak_Secnario('5_3')
        Speak_Secnario('6')

        agent.movej(basket_pos1)
        agent.movej(basket_pos2)
        agent.movel([30, 40, 30, 0, 0, 0])
        agent.movel([0, 0, 100, 0, 0, 0])
        agent.movel([0, 200, 0, 0, 0, 0])

    else:
        Speak_Secnario('5_2_n')




if __name__ == '__main__':
    try:
        agent = Agent()
        while True:
            test_case = input('what is your name : ')
            if test_case == 'yjyoo': # here is for yjyoo
                main_yjyoo(agent)
            elif test_case == 'jokim': # here is for jokim
                reload(Record_Audio)
                reload(Speech_Recognition)
                main_jokim(agent)
            if test_case == 'quit':
                break
    except Exception as e:
        print(e)