#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket

import time  # 시간관련 모듈
import math  # 계산관련 모듈

# for test
ip_addr = 'localhost'
port = 5000

def main():

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
            if command == "movej_rel":
                joints = [int(i) for i in received_data[1].split(',')]
                print('movej_rel', joints)
            if command == "movej_abs":
                joints = [int(i) for i in received_data[1].split(',')]
                print('movej_abs', joints)
            elif command == "movel_rel":
                tcp = [int(i) for i in received_data[1].split(',')]
                print('movel_rel', tcp)
            elif command == "movel_abs":
                tcp = [int(i) for i in received_data[1].split(',')]
                print('movel_abs', tcp)
            elif command == "getl":
                print('getl')
                cur_pos = [1, 2, 3, 4, 5, 6]
            elif command == "getj":
                print('getj')
                cur_pos = [7, 8, 9, 10, 11, 12]
            elif command == "open_gripper":
                print('open_gripper')
            elif command == "close_gripper":
                print('close_gripper')

            if command == 'getl' or command == 'getj':
                cur_pos = ','.join(str(j) for j in cur_pos)
                conn.send(cur_pos)
            else:
                conn.send('Success')
    except KeyboardInterrupt:  # "ctrl" + "c" 버튼 입력
        print("KeyboardInterrupt")

    except Exception as e:
        print("Error name is : {}".format(e))
    finally:
        print("finally")
        conn.send('False')
        conn.close()



if __name__ == '__main__':
    main()