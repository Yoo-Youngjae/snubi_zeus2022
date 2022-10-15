#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

# add jokim
from stt import SpeechRecognition
from stt.TextToSpeech import speak_secnario
from importlib import reload
import time
from robot_global_variable import *


def main_yjyoo(agent):
    agent.belt_on()
    agent.open_gripper()
    start_time = time.time()
    object_start_time = None
    exist_egg = False
    while time.time() - start_time <= BELT_MAX_TIME:
        if object_start_time is None:
            object_start_time = time.time()
        # 1. go home posision
        agent.movej(HOME_POS, rel=False)
        center_coordinate_list = agent.get_object_coordnates_by_vision_agent()
        if len(center_coordinate_list) == 0: # 물체 등장 없음
            print(round(time.time() - object_start_time))
            time.sleep(1)
            if time.time() - object_start_time >= BELT_STOP_TIME:  # 10 초이상 물체 등장 안함
                if exist_egg:
                    agent.movej(EGG_POS, rel=False)
                    agent.movel([0, 0, -80, 0, 0, 0])
                    agent.close_gripper()
                    agent.movel([0, 0, 100, 0, 0, 0])
                    agent.movej(PLACE_POS, rel=False)
                    agent.movel([60, 0, -350, 0, 0, 0])
                    agent.open_gripper()
                    agent.movej(PLACE_POS, rel=False)
                    agent.movej(HOME_POS, rel=False)
                break
            continue
        object_start_time = None
        target_object_x, target_object_y = center_coordinate_list[0], center_coordinate_list[1]
        object_angle, object_class = center_coordinate_list[2], center_coordinate_list[3]

        if target_object_x >250:
            continue
        print('1) objects coord', (target_object_x, target_object_y), object_angle)
        y_offset = int((target_object_y - 350) // 15 * 10)
        gripper_angle = 90 - object_angle


        # 2. detection object and get distance
        print('2) y_offset, gripper_angle', y_offset, gripper_angle)
        xyz = [-135, 90 + y_offset, 0]
        xyz += [0, 0, gripper_angle] # for rx,ry,rz
        # 3. go to the object
        agent.movel(xyz)
        z_offset = 100
        agent.movel([0, 0,-z_offset , 0, 0, 0])
        # 4. grasp
        agent.close_gripper()
        # 5. go to place position
        agent.movej(HOME_POS)
        agent.movel([0, 0, 260, 0, 0, 0])

        if int(object_class) == EGG_CLASS_NUM:
            speak_secnario('3')
            exist_egg = True
            agent.movej(EGG_POS, rel=False)
            agent.movel([0, 0, -80, 0, 0, 0])
            agent.open_gripper()
            agent.movel([0, 0, 100, 0, 0, 0])
            continue
        agent.movej(PLACE_POS, rel=False)
        # 6. go to empty place
        agent.movel([60, 0, -350, 0, 0, 0])
        # 7. release the gripper
        agent.open_gripper()
        # 8. back to the place position
        agent.movej(PLACE_POS, rel=False)

        agent.movej(HOME_POS, rel=False)

def place_motion(agent):
    basket_temp = [0, 0, 140, 5, -135, 75]
    basket_pos1 = [25, 48, 139, -125, -124, 115]
    basket_pos2 = [91, -2, 127, -78, -94, 148]
    basket_pos3 = [164, -5, 92, -88, -58, 186]

    agent.movej(HOME_POS)
    agent.movej([0, 0, 0, 0, 0, 0])
    agent.movej(basket_temp)
    agent.movej(basket_pos1)
    agent.movel([100, 120, 120, 0, 0, 0])
    agent.movel([0, 0, 170, 0, 0, 0])
    agent.movel([0, 200, 0, 0, 0, 0])
    agent.movej(basket_pos2)
    agent.movel([0, 0, -40, 0, 0, 0])
    agent.movel([10, 150, 0, 0, 0, 0])
    agent.close_gripper()
    agent.movel([0, 0, 280, 0, 0, 0])
    agent.movel([0, -120, 0, 0, 0, 0])
    agent.movel([-90, 0, -90, 0, 0, 0])
    agent.movej(basket_pos3)
    agent.open_gripper()

def main_jokim(agent):
    print("Start shopping")

    agent.movej(HOME_POS)

    speak_secnario('1')
    # speak_secnario('4')
    # speak_secnario('5_2')

    # 예 아니요 마이크 입력
    INPUT_AUDIO = "/home/snubi/PycharmProjects/snubi_zeus2022/stt/audio_data/input_audio.wav"
    Record_Audio.start(INPUT_AUDIO)
    stt = Speech_Recognition.stt(INPUT_AUDIO)

    print("Result:", stt['text'])  # text 결과 출력

    pos_list = ["예", "네", "그래", "응", "해줘", "진행해줘"]

    #if stt['text'] in pos_list:
    if "해줘" in pos_list:
        # speak_secnario('5_3')
        speak_secnario('6')

        place_motion(agent)

    else:
        speak_secnario('7')

def main_full(agent):
    while True:
        print('1. start. go to home pose')
        agent.movej(HOME_POS)
        speak_secnario('1')
        stt_res = agent.stt_controller.stt(SEC=3)
        if stt_res == 'yes':
            break
    while True:
        # detectron page
        agent.ui_page_go(2)
        print('2. belt_on. calc start')
        speak_secnario('2')
        main_yjyoo(agent)
        print('3. end calc.')
        agent.belt_off()
        speak_secnario('4')
        stt_res = agent.stt_controller.stt(SEC=3)
        if stt_res == 'yes':
            break
    agent.ui_page_go(3)
    speak_secnario('5')
    speak_secnario('6')
    place_motion(agent)
    agent.ui_page_go(4)
    speak_secnario('7')
    agent.ui_page_go(0)

if __name__ == '__main__':
    try:
        agent = Agent()
        while True:
            test_case = input('what is your name : ')
            if test_case == 'full':
                main_full(agent)
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