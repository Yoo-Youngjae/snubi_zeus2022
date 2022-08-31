#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket

# for test
ip_addr = 'localhost'
port = 5000

sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket() 소켓서버 생성
sever_socket.bind((ip_addr, port)) #서버가 사용할 IP주소와 포트번호를 생성한 소켓에 결합
sever_socket.listen(0) #소켓 서버의 클라이언트의 접속을 기다린다.
client_socket, addr = sever_socket.accept() #요청 수신되면 요청을 받아들여 데이터 통신을 위한 소켓 생성

try:
    while True: #데이터 송수신
        data = client_socket.recv(65535) #data 인스턴스 생성 및 수신
        data = data.decode()  #수신된 byte code를 문자열로 변환
        print (data) #변환된 문자열을 출력
        setdata =input("input data")
        setdata = setdata.encode() #문자열 -> byte code 변환 
        client_socket.send(setdata) #client socket으로 data 송신
except Exception as e:
    print(e)
finally:
    sever_socket.close() # 소켓통신 종료