
import socket

class Agent:
    def __init__(self):
        # for test
        ip_addr = 'localhost'
        port = 5000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket() 소켓서버 생성
        self.client_socket.connect((ip_addr, port))  # address에 있는 원격 소켓에 연결


    def send(self, data):
        data_encoded = data.encode()  # 문자열 -> byte code 변환
        self.client_socket.sendall(data_encoded)  # client socket으로 data 송신
        data = self.client_socket.recv(1024)
        print('received', data.decode())

    def movej(self, joints):

        self.send(joints)
