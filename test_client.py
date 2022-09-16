#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

home_pos = [68, -9, -102, 0, -69, 69]
gripper_pos = [98, -9, -102, 0, 111, 69]
basket_pos1 = [21, -2, 143, -86, -139, 176]
#basket_pos1 = [33, -33, 137, -54, -117, 34]
basket_pos2 = [47, 33, 152, -102, -127, 116]
#basket_pos2 = [19, 27, 127, -103, -139, 155]

if __name__ == '__main__':
    try:
        agent = Agent()
        while True:
            test_case = input('command : ')
            if test_case == 'h':
                agent.movej(home_pos)
            elif test_case == 'gripper':
                agent.movej(gripper_pos)
            elif test_case == 'w':
                agent.movel([0, 10, 0, 0, 0, 0])
            elif test_case == 's':
                agent.movel([0, -10, 0, 0, 0, 0])
            elif test_case == 'a':
                agent.movel([-10, 0, 0, 0, 0, 0])
            elif test_case == 'd':
                agent.movel([10, 0, 0, 0, 0, 0])
            elif test_case == 'r':
                agent.movel([0, 0, 10, 0, 0, 0])
            elif test_case == 'f':
                agent.movel([0, 0, -10, 0, 0, 0])
            elif test_case == 'z':
                agent.movel([0, 0, 0, 0, 0, 10])
            elif test_case == 'x':
                agent.movel([0, 0, 0, 0, 0, -10])
            elif test_case == 'p':
                agent.close_gripper()
            elif test_case == 'l':
                agent.open_gripper()
            elif test_case == 'getj':
                print('agent.getj()', agent.getj())
            elif test_case == 'getl':
                print('agent.getl()', agent.getl())
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

            elif test_case == 'q':
                break
            else:
                print('invalid command')
    except Exception as e:
        print(e)