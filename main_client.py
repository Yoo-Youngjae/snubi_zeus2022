#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

home_pos = [68, -9, -102, 0, -69, 69]
place_pos = [-26, -8, -94, 0, -78, -25]
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






if __name__ == '__main__':
    try:
        agent = Agent()
        while True:
            test_case = input('what is your name : ')
            if test_case == 'yjyoo': # here is for yjyoo
                main_yjyoo(agent)
            if test_case == 'quit':
                break
    except Exception as e:
        print(e)