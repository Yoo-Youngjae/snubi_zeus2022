#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

# add jokim
from STT.TextToSpeech import speak_secnario
import time
from robot_global_variable import *
import threading


def main_pick_and_place(agent):
    # agent.belt_on()
    agent.open_gripper()
    start_time = time.time()
    agent.movej(HOME_POS, rel=False)
    time.sleep(3)
    object_start_time = None
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
                return
            continue
        object_start_time = None
        target_object_x, target_object_y = center_coordinate_list[0], center_coordinate_list[1]
        object_angle, object_class = center_coordinate_list[2], center_coordinate_list[3]

        if target_object_x < 1035:
            print('1-1) objects coord is too far to pick', (target_object_x, target_object_y), object_angle)
            continue
        print('1) objects coord', (target_object_x, target_object_y), object_angle)
        # vision_robot calibration
        x_offset = -145
        y_offset = int((360 - target_object_y) // (174 / 90)) + 95
        z_offset = 95
        gripper_angle = 90 - object_angle
        if int(object_class) == MILK_CLASS_NUM:
            x_offset = -160


        # 2. detection object and get distance
        print('2) x_offset, y_offset, gripper_angle', x_offset, y_offset, gripper_angle)
        xyz = [x_offset, y_offset, 0]
        xyz += [0, 0, gripper_angle] # for rx,ry,rz
        # 3. go to the object
        agent.movel(xyz)

        agent.movel([0, 0, -z_offset, 0, 0, 0])
        # 4. grasp
        # test_mode = False
        # if test_mode:
        #     time.sleep(3)
        #     continue
        #################################
        agent.close_gripper()
        # 5. go to place position
        agent.movej(HOME_POS)

        if int(object_class) == EGG_CLASS_NUM:
            agent.movel([0, 0, 260, 0, 0, 0])
            speak_secnario('3-2')
            agent.exist_egg = True
            agent.movej(EGG_POS, rel=False)
            agent.movel([0, 0, -80, 0, 0, 0])
            agent.open_gripper()
            agent.movel([0, 0, 100, 0, 0, 0])
            continue
        elif int(object_class) == MILK_CLASS_NUM:
            speak_secnario('3-3')
            agent.movej(HOME_POS)
            pass_though(agent)
            continue
        else:
            agent.movel([0, 0, 260, 0, 0, 0])
            agent.movej(PLACE_POS, rel=False)
            # 6. go to empty place
            agent.movel([60, 0, -350, 0, 0, 0])
            # 7. release the gripper
            agent.open_gripper()
            # 8. back to the place position
            agent.movej(PLACE_POS, rel=False)

            agent.movej(HOME_POS, rel=False)

    return agent.exist_egg
def pass_though(agent):
    pass_though1 = [68, 0, -180, 0, 110, 0]
    pass_though1 = [68, 0, -180, 0, 110, 0]
    pass_though2 = [28, 0, -235, 0, 50, 0]
    pass_though3 = [38, 0, -180, 0, -110, 0]


    agent.movej(pass_though1)
    agent.movej(pass_though2)
    agent.open_gripper()
    time.sleep(2)
    agent.close_gripper()
    agent.movej(pass_though3)
    agent.movej(HOME_POS)
    agent.open_gripper()

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
    agent.movel([0, 0, -50, 0, 0, 0])
    agent.movel([15, 150, 0, 0, 0, 0])
    agent.close_gripper()
    agent.movel([0, 0, 290, 0, 0, 0])
    agent.movel([0, -120, 0, 0, 0, 0])
    agent.movel([-95, 0, -90, 0, 0, 0])
    agent.movej(basket_pos3)
    agent.open_gripper()

def return_place_motion(agent):
    agent.open_gripper()
    agent.movej([0, 0, 0, 0, 0, 0])
    agent.movej(HOME_POS)


def welcome_motion(agent):
    welcome_pose1 = [55, -15, -97, 0, 109, 49]
    welcome_pose2 = [47, -24, -110, 0, 79, 90]

    agent.movej(HOME_POS)

    agent.movej(welcome_pose1)
    agent.movej([0, 0, 0, 0, 10, 0], rel=True)
    agent.movej([0, 0, 0, 0, -20, 0], rel=True)
    agent.movej([0, 0, 0, 0, 20, 0], rel=True)
    agent.movej([0, 0, 0, 0, -20, 0], rel=True)

    # agent.movel([150, 0, 0, 0, 0, 0], rel=True)
    # agent.movel([-150, 0, -150, 0, 0, 0], rel=True)
    # agent.movel([150, 0, 0, 0, 0, 0], rel=True)

    agent.movej(welcome_pose2)
    agent.close_gripper()
    agent.open_gripper()
    agent.close_gripper()
    agent.open_gripper()

def place_egg(agent):
    agent.movej(EGG_POS, rel=False)
    agent.movel([0, 0, -80, 0, 0, 0])
    agent.close_gripper()
    agent.movel([0, 0, 100, 0, 0, 0])
    agent.movej(PLACE_POS, rel=False)
    agent.movel([60, 0, -350, 0, 0, 0])
    agent.open_gripper()
    agent.movej(PLACE_POS, rel=False)
    agent.movej(HOME_POS, rel=False)



def main_full(agent):
    agent.movej(HOME_POS)
    t = threading.Thread(target=speak_secnario, args=('1',))
    t.start()
    time.sleep(2)
    welcome_motion(agent)
    while True:
        print('1. start. go to home pose')
        agent.movej(HOME_POS)
        detected_user_id = agent.detect_face_id()
        if detected_user_id != -1:
            agent.user_id_go(detected_user_id)
            break
    print('1-2. detected_user_id', detected_user_id)

    # 2. user detection & welcome motion
    time.sleep(2)
    agent.ui_page_go(2)
    speak_secnario('2', detected_user_id)
    # detectron page
    agent.ui_page_go(3)

    motion_up_test_mode = True
    while True:
        agent.belt_on()
        if motion_up_test_mode:
            agent.motionparam_up()
        print('2. belt_on. calc start')
        speak_secnario('3-1')
        main_pick_and_place(agent)
        print('3. end calc.')
        agent.belt_off()
        if motion_up_test_mode:
            agent.motionparam_down()
        speak_secnario('3-4')
        stt_res = agent.stt_controller.stt(SEC=3)
        if stt_res == 'yes':
            break

    # egg go to basket
    if agent.exist_egg:
        speak_secnario('3-5')
        place_egg(agent)

    agent.ui_page_go(4)
    speak_secnario('4')
    place_motion(agent)
    agent.ui_page_go(5)
    speak_secnario('5')
    agent.ui_page_go(1)

def main_custom(agent):
    agent.movej(HOME_POS)
    t = threading.Thread(target=speak_secnario, args=('1',))
    t.start()
    time.sleep(2)
    welcome_motion(agent)

    print('1. start. go to home pose')
    agent.movej(HOME_POS)
    detected_user_id = 3
    agent.user_id_go(detected_user_id)

    print('1-2. detected_user_id', detected_user_id)
    # 2. user detection & welcome motion
    time.sleep(2)
    agent.ui_page_go(2)
    speak_secnario('2', detected_user_id)
    # detectron page
    agent.ui_page_go(3)
    while True:
        agent.belt_on()
        print('2. belt_on. calc start')
        speak_secnario('3-1')
        main_pick_and_place(agent)
        print('3. end calc.')
        agent.belt_off()
        speak_secnario('3-4')
        stt_res = agent.stt_controller.stt(SEC=3)
        if stt_res == 'yes':
            break

    # egg go to basket
    if agent.exist_egg:
        speak_secnario('3-5')
        place_egg(agent)

    agent.ui_page_go(4)
    speak_secnario('4')
    place_motion(agent)
    agent.ui_page_go(5)
    speak_secnario('5')
    agent.ui_page_go(1)

if __name__ == '__main__':
    try:
        agent = Agent()
        while True:
            test_case = input('Select scenario : ')
            if test_case == 'full':
                agent.init_variable()
                main_full(agent)
                agent.belt_off()
            if test_case == 'custom':
                agent.init_variable()
                main_custom(agent)
                agent.belt_off()
            if test_case == 'pp':
                agent.belt_on()
                main_pick_and_place(agent)
                agent.belt_off()
            if test_case == 'basket':
                place_motion(agent)
            if test_case == 'return_basket':
                return_place_motion(agent)
            if test_case == 'quit' or test_case == 'q':
                break
    except Exception as e:
        print(e)
    finally:
        agent.belt_off()