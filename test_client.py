#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent
import serial
import time

home_pos = [68, -9, -102, 0, -69, 69]
home_pos2 = [68, -9, -102, 0, 30, 0]
place_pos = [-48, 3, -60, 0, -121, -47]

gripper_pos = [98, -9, -102, 0, 111, 69]
gripper_pos2 = [98, -9, -102, 0, 111, 69-180]
basket_pos1 = [21, -2, 143, -86, -139, 176]
#basket_pos1 = [33, -33, 137, -54, -117, 34]
basket_pos2 = [47, 33, 152, -102, -127, 116]
#basket_pos2 = [19, 27, 127, -103, -139, 155]

if __name__ == '__main__':
    try:
        agent = Agent()
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        while True:
            test_case = input('command : ')
            if test_case == 'h':
                agent.movej(home_pos)
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
                agent.movel([0, 0, -103, 0, 0, 0])
                agent.close_gripper()
                agent.movej(home_pos)
                agent.open_gripper()
            elif test_case == 'place':
                agent.movej(home_pos)
                agent.movel([0, 0, 200, 0, 0, 0])
                agent.movej(place_pos)
                agent.open_gripper()
                agent.movej(place_pos)
            elif test_case == 'pp':
                agent.movej(home_pos)
                agent.open_gripper()
                agent.movel([-90, 90, 0, 0, 0, 0])
                agent.movel([0, 0, -103, 0, 0, 0])
                agent.close_gripper()
                agent.movej(home_pos)
                agent.movel([0, 0, 260, 0, 0, 0])
                agent.movej(place_pos)
                agent.open_gripper()
                agent.movej(place_pos)
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
                agent.movej(basket_pos1)
                agent.movej(basket_pos2)
                agent.movel([30, 30, 30, 0, 0, 0])
                agent.movel([0, 0, 100, 0, 0, 0])
                agent.movel([0, 200, 0, 0, 0, 0])
                #agent.movel([0, 0, 0, 30, 0, 0])
            elif test_case == 'belt_on':
                if ser.readable():
                    ser.write('1'.encode('utf-8'))
                    time.sleep(0.5)
            elif test_case == 'belt_off':
                if ser.readable():
                    ser.write('0'.encode('utf-8'))
                    time.sleep(0.5)
            elif test_case == 'q':
                break
            else:
                print('invalid command')
    except Exception as e:
        print(e)