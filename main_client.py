#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

# add jokim
from stt import Speech_Recognition, Record_Audio
from stt.Text_to_Speech import Speak_Secnario
from importlib import reload
import time

# global variable
home_pos = [68, -9, -102, 0, -69, 69]
place_pos = [-48, 3, -60, 0, -121, -47]

INPUT_AUDIO = "/home/snubi/PycharmProjects/snubi_zeus2022/stt/audio_data/input_audio.wav"
basket_pos1 = [21, -2, 143, -86, -139, 176]
basket_pos2 = [47, 33, 152, -102, -127, 116]
# basket_pos1 = [33, -33, 137, -54, -117, 34]
# basket_pos2 = [19, 27, 127, -103, -139, 155]

def main_yjyoo(agent):
    print("1. Start shopping")
    agent.belt_on()
    agent.open_gripper()
    start_time = time.time()
    while time.time() - start_time <= 180:
        # 1. go home posision
        agent.movej(home_pos, rel=False)
        center_coordinate_list = agent.get_object_coordnates_by_vision_agent()
        if len(center_coordinate_list) == 0:
            continue

        target_object_x, target_object_y = center_coordinate_list[0], center_coordinate_list[1]
        object_angle = center_coordinate_list[2]
        if target_object_x >250:
            continue
        print('1. objects coord', (target_object_x, target_object_y), object_angle)
        y_offset = int((target_object_y - 350) // 15 * 10)
        gripper_angle = 90 - object_angle


        # 2. detection object and get distance
        print('2. y_offset, gripper_angle', y_offset, gripper_angle)
        xyz = [-135, 90 + y_offset, 0]
        xyz += [0, 0, gripper_angle] # for rx,ry,rz
        # 3. go to the object
        agent.movel(xyz)
        z_offset = 100
        agent.movel([0, 0,-z_offset , 0, 0, 0])
        # 4. grasp
        agent.close_gripper()
        # 5. go to place position
        agent.movel([0, 0, +z_offset, 0, 0, 0])
        agent.movej(place_pos, rel=False)
        # 6. go to empty place
        agent.movel([0, 0, -100, 0, 0, 0])
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
            if test_case == 'quit' or test_case == 'q':
                break
    except Exception as e:
        print(e)
    finally:
        agent.belt_off()