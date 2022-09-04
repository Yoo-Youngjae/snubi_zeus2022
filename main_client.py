#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

home_pose = [0, 0, 0, 0, 0, 0]

def main_yjyoo(agent):
    agent.movej(home_pose, rel=False)




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