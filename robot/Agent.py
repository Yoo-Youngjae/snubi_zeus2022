import socket
import serial
import time
from vision_module.vision_controller import VisionController
class Agent:
    def __init__(self):
        # for connect robot
        ip_addr = '192.168.0.23'
        port = 5000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket() 소켓서버 생성
        self.client_socket.connect((ip_addr, port))  # address에 있는 원격 소켓에 연결
        # for connect arduino
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        self.vision_controller = VisionController()

    def __del__(self):
        self.client_socket.close() # 소켓통신 종료


    def send(self, data):
        data_encoded = data.encode()  # 문자열 -> byte code 변환
        self.client_socket.sendall(data_encoded)  # client socket으로 data 송신
        data = self.client_socket.recv(1024)
        return data.decode()

    def movej(self, joints, rel=False):
        if rel is True:
            msg = 'movej_rel '
            msg += ','.join(str(j) for j in joints)
            self.send(msg)
        else:
            msg = 'movej_abs '
            msg += ','.join(str(j) for j in joints)
            self.send(msg)

    def movel(self, tcp, rel=True):
        if rel is True:
            msg = 'movel_rel '
            msg += ','.join(str(j) for j in tcp)
            self.send(msg)
        else:
            msg = 'movel_abs '
            msg += ','.join(str(j) for j in tcp)
            self.send(msg)

    def getl(self):
        pos = self.send('getl ')

        # return [int(i) for i in pos.split(',')]

    def getj(self):
        pos = self.send('getj ')

        # return [int(i) for i in pos.split(',')]

    def open_gripper(self):
        self.send('open_gripper')

    def close_gripper(self):
        self.send('close_gripper')

    def belt_on(self):
        if self.ser.readable():
            self.ser.write('1'.encode('utf-8'))
            time.sleep(0.5)
    def belt_off(self):
        if self.ser.readable():
            self.ser.write('0'.encode('utf-8'))
            time.sleep(0.5)

