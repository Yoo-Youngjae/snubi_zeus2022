#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.Agent import Agent

home_pose = [0, 0, 0, 0, 0, 0]

if __name__ == '__main__':
    try:
        agent = Agent()
        agent.movej(home_pose, rel=True)

    except Exception as e:
        print(e)
    finally:
        agent.client_socket.close()  # 소켓통신 종료