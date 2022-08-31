#!/usr/bin/python
# -*- coding: utf-8 -*-
## 1. 초기 설정① #######################################
# 라이브러리 가져오기
## 1．초기 설정 ①　모듈 가져오기 ######################
from i611_MCS import *
from teachdata import *
from i611_extend import *
from rbsys import *
from i611_common import *
from i611_io import *
from i611shm import * 
import socket

def main():
    ## 2. 초기 설정② ####################################
    # ZERO 로봇 생성자 
    rb = i611Robot()
    # 좌표계의 정의
    _BASE = Base()
    # 로봇과 연결 시작 초기화
    rb.open()
    # I/O 입출력 기능의 초기화 
    IOinit( rb )
    # 교시 데이터 파일 읽기
    data = Teachdata( "teach_data" )
    ## 1. 교시 포인트 설정 ######################
    p1 = Position( -418.30, -398.86, 287.00, 0, 0, -180 )
    p2 = Position( -158.54, -395.10, 287.00, 0, 0, -180 )
    ## 2. 동작 조건 설정 ######################## 
    m = MotionParam( jnt_speed=10, lin_speed=10, pose_speed=10, overlap = 30 )
    #MotionParam 형으로 동작 조건 설정
    rb.motionparam( m )
   
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #INET은 주소패밀리의 기본값, SOCK_STREAM은 소켓 유형의 기본값
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1) #(level, optname, value: int) 주어진 소켓 옵션의 값을 설정
    sock.connect(('192.168.0.20',5000)) #address에 있는 원격 소켓에 연결
    
    ## 3. 로봇 동작을 정의 ##############################
    # 작업 시작
    Socket_data = 'start' #data 인스턴스 생성
    Socket_data = Socket_data.encode() # 유니코드를 utf-8, euc-kr, ascii 형식의 byte코드로 변환
    sock.send(Socket_data) #data 전송 

    while True:
            
        Socket_data = sock.recv(65535) #server socket으로부터 data 수신
        Socket_data = Socket_data.decode() #byte code -> 문자열 변환
        print Socket_data #변환된 문자열 출력
        rb.sleep(1)

        if Socket_data =="1": #input data를 1로 입력시 
            sock.send("p1") #data 전송, p1이 print된다.

        elif Socket_data =="2": #input data를 2로 입력시
            sock.send("p2") #data 전송, p2가 print된다.

    ## 4. 종료 ######################################
    # 로봇과의 연결을 종료
    rb.close()
if __name__ == '__main__':
    main()