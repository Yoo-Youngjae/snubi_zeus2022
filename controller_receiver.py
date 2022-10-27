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
from threading import Event # event 모듈
import socket

import os # 운영체제 모듈
import time # 시간관련 모듈
import math # 계산관련 모듈

# for test
ip_addr = '192.168.0.23'
port = 5000

def th_stop(event):   # thread 함수
    while True:
        if event.is_set():
            return
        if din(9) == '1': # din(9) = 1일 때 프로그램 종료
            print("User Program Stop!")
            pid = os.getpid()
            os.kill(pid, signal.SIGTERM)    #os signal.SIGKILL
        time.sleep(0.1)

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
    try:
        rb.open()
    except:
        ans = input("Turn on the servo man! Did you turn it on?(y/n) >> ")
        if ans == 'y':
            rb.open()
        else:
            print("You didn't turn it on man...")
            return
    # I/O 입출력 기능의 초기화 
    IOinit(rb)
    # x 3
    motion = MotionParam(jnt_speed=30, lin_speed=450, pose_speed=60, acctime=0.4, dacctime=0.4, overlap=20)

    # motion = MotionParam(jnt_speed=10, lin_speed=150, pose_speed=20, acctime=0.1, dacctime=0.1, overlap=20)
    #MotionParam 형으로 동작 조건 설정
    rb.motionparam(motion)

    event = Event()
    th = threading.Thread(target=th_stop, args=(event,))  # def된 함수를 thread 생성
    th.setDaemon(True)  # main 함수와 같이 시작하고 끝나도록 daemon 함수로 설정 (병렬동작이 가능하도록 하는 기능)
    th.start()  # thread 동작
    print('Start Server Node...')

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # INET은 주소패밀리의 기본값, SOCK_STREAM은 소켓 유형의 기본값
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF,
                                 1)  # (level, optname, value: int) 주어진 소켓 옵션의 값을 설정
        server_socket.bind((ip_addr, port))  # 서버가 사용할 IP주소와 포트번호를 생성한 소켓에 결합
        server_socket.listen(0)  # 소켓 서버의 클라이언트의 접속을 기다린다.

        conn, addr = server_socket.accept()  # 요청 수신되면 요청을 받아들여 데이터 통신을 위한 소켓 생성
        while True:
            received_data = conn.recv(1024)  # server socket으로부터 data 수신
            received_data = received_data.decode()  # byte code -> 문자열 변환
            received_data = received_data.split(' ')
            command = received_data[0]
            if command == "movej_rel":
                joints = [int(i) for i in received_data[1].split(',')]
                print('movej_rel', joints)
                rb.reljntmove(dj1=joints[0], dj2=joints[1], dj3=joints[2], dj4=joints[3], dj5=joints[4], dj6=joints[5])
            elif command == "movej_abs":
                joints = [int(i) for i in received_data[1].split(',')]
                print('movej_abs', joints)
                rb.move(Joint(joints[0], joints[1], joints[2], joints[3], joints[4], joints[5]))
            elif command == "movel_rel":
                tcp = [int(i) for i in received_data[1].split(',')]
                print('movel_rel', tcp)
                rb.relline(dx=tcp[0], dy=tcp[1], dz=tcp[2], drx=tcp[3], dry=tcp[4], drz=tcp[5])
            elif command == "movel_abs":
                tcp = [int(i) for i in received_data[1].split(',')]
                rb.optline(Position(tcp[0], tcp[1], tcp[2], tcp[5], tcp[4], tcp[3]))
                print('movel_abs', tcp)
            elif command == "getl":
                current_xy_coordi()
                # cur_pos = current_xy_coordi()
            elif command == "getj":
                current_joint_coordi()
                # cur_pos = current_joint_coordi()
            elif command == "open_gripper":
                print('open_gripper')
                clamp_(2)
            elif command == "close_gripper":
                print('close_gripper')
                clamp_(1)
            elif command == "motionparam_up":   # x4
                motion = MotionParam(jnt_speed=40, lin_speed=600, pose_speed=80, acctime=0.4, dacctime=0.4, overlap=20)
                rb.motionparam(motion)
            elif command == "motionparam_down": # x3
                motion = MotionParam(jnt_speed=30, lin_speed=450, pose_speed=60, acctime=0.4, dacctime=0.4, overlap=20)
                rb.motionparam(motion)
            else:
                print('invalid format', command)

            # if command == 'getl' or command == 'getj':
            #     cur_pos = ','.join(str(j) for j in cur_pos)
            #     conn.send(cur_pos)
            # else:
            conn.send('Success')
    except KeyboardInterrupt:           # "ctrl" + "c" 버튼 입력
        print("KeyboardInterrupt")
    except Robot_emo:
        print("Robot_emo")
    except Exception as e:
        print("Error name is : {}".format(e))
    finally:
        print("finally")
        conn.close()
        dout(48, '000')

    ## 4. 종료 ######################################
    # 로봇과의 연결을 종료
    event.set()
    rb.close()
if __name__ == '__main__':
    main()