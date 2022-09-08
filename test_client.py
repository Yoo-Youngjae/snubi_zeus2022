#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

home_pos = [0,0,0,0,0,0]
if __name__ == '__main__':
    try:
        agent = Agent()
        while True:
            test_case = input('command : ')
            if test_case == 'h':
                agent.movej(home_pos)
            elif test_case == 'w':
                agent.movel([0, 0.1, 0, 0, 0, 0])
            elif test_case == 's':
                agent.movel([0, -0.1, 0, 0, 0, 0])
            elif test_case == 'a':
                agent.movel([-0.1, 0, 0, 0, 0, 0])
            elif test_case == 'd':
                agent.movel([0.1, 0, 0, 0, 0, 0])
            elif test_case == 'r':
                agent.movel([0, 0, 0.1, 0, 0, 0])
            elif test_case == 'f':
                agent.movel([0, 0, -0.1, 0, 0, 0])
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
            elif test_case == 'q':
                break
            else:
                print('invalid command')
    except Exception as e:
        print(e)