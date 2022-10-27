#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent
import serial
import time
from robot_global_variable import *
from STT.TextToSpeech import speak_secnario
import threading

home_pos = [68, -9, -102, 0, -69, 69]
# home_pos = [55, -5, -102, 0, -73, 56]
home_pos2 = [68, -9, -102, 0, 30, 0]
place_pos = [-46, -8, -65, 0, -106, -45]

gripper_pos = [98, -9, -102, 0, 111, 69]
gripper_pos2 = [98, -9, -102, 0, 111, 69-180]

basket_temp = [0, 0, 140, 5, -135, 75]
basket_pos1 = [25, 48, 139, -125, -124, 115]
basket_pos2 = [91, -2, 127, -78, -94, 148]
basket_pos3 = [164, -5, 92, -88, -58, 186]


pass_though1 = [68, 0, -180, 0, 110, 0]
pass_though2 = [23, 0, -235, 0, 50, 0]
pass_though3 = [38, 0, -180, 0, -110, 0]


# j1=38.0, j2=-9.0, j3=-220.0, j4=0.0, j5=30.0, j6=0.0
#basket_pos1 = [96, -24, 149, -55, -106, 198] 간지
#basket_pos2 = [37, 0, 90, 0, -90, 56]

if __name__ == '__main__':
    try:
        agent = Agent()
        ser = serial.Serial(BELT_USB_PORT, 9600)
        while True:
            test_case = input('command : ')
            if test_case == 'h':
                agent.movej(home_pos)
            elif test_case == 'place':
                agent.movej(place_pos)
            elif test_case == 'egg':
                agent.movej(EGG_POS)
                agent.movel([0, 0, -80, 0, 0, 0])
                agent.close_gripper()
                agent.movel([0, 0, 80, 0, 0, 0])
            elif test_case == 'pass_though_go':
                agent.movej(pass_though1)
                agent.movej(pass_though2)
            elif test_case == 'pass_though_back':
                agent.movej(pass_though3)
                agent.movej(HOME_POS)
            elif test_case == 'pass_though1':
                agent.movej(pass_though1)
            elif test_case == 'pass_though2':
                agent.movej(pass_though2)
            elif test_case == 'h2':
                agent.movej(home_pos2)
            elif test_case == 'gripper':
                agent.movej(gripper_pos)
            elif test_case == 'gripper2':
                agent.movej(gripper_pos2)
            elif test_case == 'w':
                agent.movel([0, 30, 0, 0, 0, 0])
            elif test_case == 's':
                agent.movel([0, -30, 0, 0, 0, 0])
            elif test_case == 'a':
                agent.movel([-30, 0, 0, 0, 0, 0])
            elif test_case == 'd':
                agent.movel([30, 0, 0, 0, 0, 0])
            elif test_case == 'r':
                agent.movel([0, 0, 30, 0, 0, 0])
            elif test_case == 'f':
                agent.movel([0, 0, -30, 0, 0, 0])
            elif test_case == 'z':
                agent.movel([0, 0, 0, 0, 0, 30])
            elif test_case == 'x':
                agent.movel([0, 0, 0, 0, 0, -30])
            elif test_case == '8':
                agent.movel([0, 10, 0, 0, 0, 0])
            elif test_case == '5':
                agent.movel([0, -10, 0, 0, 0, 0])
            elif test_case == '4':
                agent.movel([-10, 0, 0, 0, 0, 0])
            elif test_case == '6':
                agent.movel([10, 0, 0, 0, 0, 0])
            elif test_case == '9':
                agent.movel([0, 0, 10, 0, 0, 0])
            elif test_case == '7':
                agent.movel([0, 0, -10, 0, 0, 0])
            elif test_case == 'p':
                agent.close_gripper()
            elif test_case == 'l':
                agent.open_gripper()
            elif test_case == 'getj':
                agent.getj()
            elif test_case == 'getl':
                agent.getl()
            elif test_case == 'pick':
                agent.movej(home_pos)
                agent.movel([-90, 90, 0, 0, 0, 0])
                agent.movel([0, 0, -95, 0, 0, 0])
                continue
                agent.close_gripper()
                agent.movej(home_pos)
                agent.open_gripper()
            elif test_case == 'pick20':
                for i in range(20):
                    agent.movej(home_pos)
                    agent.movel([-90, 90, 0, 0, 0, 0])
                    agent.movel([0, 0, -95, 0, 0, 0])
                    agent.close_gripper()
                    agent.movej(home_pos)
                    agent.open_gripper()
            elif test_case == 'pp':
                agent.movej(home_pos)
                agent.open_gripper()
                agent.movel([-160, 40, 0, 0, 0, 0])
                agent.movel([0, 0, -120, 0, 0, 0])
                agent.close_gripper()
                agent.movej(home_pos)
                agent.movel([0, 0, 260, 0, 0, 0])
                agent.movej(place_pos)
                agent.open_gripper()
                agent.movel([-120, 0, 0, 0, 0, 0])
                agent.movej(home_pos)
            elif test_case == 'pn':
                z_dist = int(input('z_dist : '))
                agent.movel([0, 0, -z_dist, 0, 0, 0])
            elif test_case == 'movel_rel':
                tcp = input('x,y,z,rx,ry,rz')
                tcp = [int(t) for t in tcp.split(',')]
                if len(tcp) == 3:
                    tcp += [0, 0, 0]
                agent.movel(tcp)
            elif test_case == 'movej_abs':
                joints = input('j1,j2,j3,j4,j5,j6')
                joints = [int(j) for j in joints.split(',')]
                agent.movej(joints)
            elif test_case == 'basket':
                agent.movej(home_pos)
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

            elif test_case == 'welcome':
                welcome_pose1 = [55, -15, -97, 0, 109, 49]
                welcome_pose2 = [47, -24, -110, 0, 79, 90]

                agent.movej(HOME_POS)

                t = threading.Thread(target=speak_secnario, args=('1',))
                t.start()
                agent.movej(welcome_pose1)
                agent.movej([0, 0, 0, 0, 10, 0], rel=True)
                agent.movej([0, 0, 0, 0, -20, 0], rel=True)
                agent.movej([0, 0, 0, 0, 20, 0], rel=True)
                agent.movej([0, 0, 0, 0, -10, 0], rel=True)

                agent.movel([150, 0, 0, 0, 0, 0], rel=True)
                agent.movel([-150, 0, -150, 0, 0, 0], rel=True)
                agent.movel([150, 0, 0, 0, 0, 0], rel=True)

                agent.movej(welcome_pose2)
                agent.close_gripper()
                agent.open_gripper()
                agent.close_gripper()
                agent.open_gripper()

            elif test_case == 'belt_on':
                if ser.readable():
                    ser.write('1'.encode('utf-8'))
                    time.sleep(0.5)
            elif test_case == 'belt_off':
                if ser.readable():
                    ser.write('0'.encode('utf-8'))
                    time.sleep(0.5)
            elif test_case == 'movej_1+':
                agent.movej([30, 0, 0, 0, 0, 0], rel=True)
            elif test_case == 'movej_1-':
                agent.movej([-30, 0, 0, 0, 0, 0], rel=True)
            elif test_case == 'movej_2+':
                agent.movej([0, 30, 0, 0, 0, 0], rel=True)
            elif test_case == 'movej_2-':
                agent.movej([0, -30, 0, 0, 0, 0], rel=True)
            elif test_case == 'movej_3+':
                agent.movej([0, 0, 30, 0, 0, 0], rel=True)
            elif test_case == 'movej_3-':
                agent.movej([0, 0, -30, 0, 0, 0], rel=True)
            elif test_case == 'movej_4+':
                agent.movej([0, 0, 0, 30, 0, 0], rel=True)
            elif test_case == 'movej_4-':
                agent.movej([0, 0, 0, -30, 0, 0], rel=True)
            elif test_case == 'movej_5+':
                agent.movej([0, 0, 0, 0, 30, 0], rel=True)
            elif test_case == 'movej_5-':
                agent.movej([0, 0, 0, 0, -30, 0], rel=True)
            elif test_case == 'movej_6+':
                agent.movej([0, 0, 0, 0, 0, 30], rel=True)
            elif test_case == 'movej_6-':
                agent.movej([0, 0, 0, 0, 0, -30], rel=True)
            elif test_case == 'sky':
                agent.movej([0, 0, 0, 0, 0, 0], rel=False)
            elif test_case == 'snake':
                agent.movej([0, 0, 0, 0, 0, 0], rel=False)
                for i in range(10):
                    agent.movej([0, 30, -60, 0, -30, 0], rel=False)
                    agent.movej([0, -30, 60, 0, 30, 0], rel=False)
            elif test_case == 'nyamnyam':
                for i in range(20):
                    agent.close_gripper()
                    agent.open_gripper()
            elif test_case == 'zeus' :
                agent.movej([90,0,-180,0,180,0],rel=False)
                time.sleep(2)
                agent.movej([42, 0, -110, 0, 21, 0], rel=False)
                time.sleep(10)
                for i in range(10) :
                    agent.movel([250, 0, 0, 0, 0, 0], rel=True)
                    agent.movel([-250, 0, -250, 0, 0, 0], rel=True)
                    agent.movel([250, 0, 0, 0, 0, 0], rel=True)
                    agent.movel([-250, 0, 0, 0, 0, 0], rel=True)
                    agent.movel([250, 0, 250, 0, 0, 0], rel=True)
                    agent.movel([-250, 0, 0, 0, 0, 0], rel=True)
            elif test_case == 'handMeThat' :
                agent.movej(home_pos)
                agent.open_gripper()
                agent.movel([-160, 40, 0, 0, 0, 0])
                agent.movel([0, 0, -95, 0, 0, 0])
                agent.close_gripper()
                agent.movej(home_pos)
                agent.movej([125,-9,-102,0,-43,83], rel=False)

            elif test_case == 'q':
                break
            else:
                print('invalid command')
    except Exception as e:
        print(e)