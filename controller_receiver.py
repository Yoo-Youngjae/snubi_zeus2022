#!/usr/bin/python
# -*- coding: utf-8 -*-
## 1. 초기 설정① #######################################
# 라이브러리 가져오기
## 1．초기 설정 ①　모듈 가져오기 ######################
from i611_MCS import *
from i611_extend import *
from rbsys import *
from i611_common import *
from i611_io import *
from i611shm import * 
import socket

import time # 시간관련 모듈
import math # 계산관련 모듈

# for test
ip_addr = 'localhost'
port = 5000


def clamp_(_mode): # clamp 가 1이라면 dout(48) 출력, 그 외 값은 dout(50) 출력
    if _mode == 1:
        dout(48, '1')
        # dout(48, '001')
    else:
        dout(50, '1')
        # dout(48, '100')
    time.sleep(0.25)
    dout(48, '000')
    time.sleep(0.25)



def current_joint_coordi():
    joint_list = shm_read( 0x3050, 6 ).split( ',' )
    joint_list[0] = round(math.degrees(float(joint_list[0])),3) # Joint 좌표계 J1 위치
    joint_list[1] = round(math.degrees(float(joint_list[1])),3) # Joint 좌표계 J2 위치
    joint_list[2] = round(math.degrees(float(joint_list[2])),3) # Joint 좌표계 J3 위치
    joint_list[3] = round(math.degrees(float(joint_list[3])),3) # Joint 좌표계 J4 위치
    joint_list[4] = round(math.degrees(float(joint_list[4])),3) # Joint 좌표계 J5 위치
    joint_list[5] = round(math.degrees(float(joint_list[5])),3) # Joint 좌표계 J6 위치
    # print joint_list # joint location 출력
    print("j1={0}, j2={1}, j3={2}, j4={3}, j5={4}, j6={5}".format(\
        joint_list[0], joint_list[1], joint_list[2], joint_list[3], joint_list[4], joint_list[5]))

def current_xy_coordi():
    position_list = shm_read( 0x3000, 6).split(',')
    position_list[0] = round(float(position_list[0])*1000,3) # XY 좌표계 X 위치
    position_list[1] = round(float(position_list[1])*1000,3) # XY 좌표계 Y 위치
    position_list[2] = round(float(position_list[2])*1000,3) # XY 좌표계 Z 위치
    position_list[3] = round(math.degrees(float(position_list[3])),3) # XY 좌표계 Rz 위치
    position_list[4] = round(math.degrees(float(position_list[4])),3) # XY 좌표계 Ry 위치
    position_list[5] = round(math.degrees(float(position_list[5])),3) # XY 좌표계 Rx 위치
    posture = shm_read( 0x3040, 1).split(',')
    position_list.append(int(posture[0])) # posture 값, list에 추가
    # print position_list # position location 출력
    print("x={0}, y={1}, z={2}, rz={3}, ry={4}, rx={5}, posture={6}".format(\
        position_list[0], position_list[1], position_list[2], position_list[3], position_list[4], position_list[5], position_list[6]))
    return position_list

def main():
    ## 2. 초기 설정② ####################################
    # ZERO 로봇 생성자 
    rb = i611Robot()
    # 좌표계의 정의
    _BASE = Base()
    # 로봇과 연결 시작 초기화
    rb.open()
    # I/O 입출력 기능의 초기화 
    IOinit(rb)
    motion = MotionParam(jnt_speed=10, lin_speed=150, pose_speed=20, acctime=0.4, dacctime=0.4, overlap=20)
    #MotionParam 형으로 동작 조건 설정
    rb.motionparam(motion)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # INET은 주소패밀리의 기본값, SOCK_STREAM은 소켓 유형의 기본값
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1)  # (level, optname, value: int) 주어진 소켓 옵션의 값을 설정
    server_socket.bind((ip_addr, port))  # 서버가 사용할 IP주소와 포트번호를 생성한 소켓에 결합
    server_socket.listen(0)  # 소켓 서버의 클라이언트의 접속을 기다린다.

    conn, addr = server_socket.accept()  # 요청 수신되면 요청을 받아들여 데이터 통신을 위한 소켓 생성

    try:
        while True:
            received_data = conn.recv(1024)  # server socket으로부터 data 수신
            received_data = received_data.decode()  # byte code -> 문자열 변환
            received_data = received_data.split(' ')

            command = received_data[0]
            if command == "movej":
                print('movej')
            elif command == "movel":
                print('movel')
            elif command == "getl":
                print('getl')
            elif command == "getj":
                print('getj')
            elif command == "open_gripper":
                print('open_gripper')
            elif command == "close_gripper":
                print('close_gripper')

    except KeyboardInterrupt:           # "ctrl" + "c" 버튼 입력
        print("KeyboardInterrupt")
    # except Robot_emo:
    #     print("Robot_emo")
    except Exception as e:
        print("Error name is : {}".format(e))
    finally:
        print("finally")
        dout(48, '000')

    ## 4. 종료 ######################################
    # 로봇과의 연결을 종료
    rb.close()
if __name__ == '__main__':
    main()