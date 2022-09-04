
import socket

class Agent:
    def __init__(self):
        # for test
        ip_addr = 'localhost'
        port = 5000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket() 소켓서버 생성
        self.client_socket.connect((ip_addr, port))  # address에 있는 원격 소켓에 연결

    def __del__(self):
        self.client_socket.close() # 소켓통신 종료


    def send(self, data):
        data_encoded = data.encode()  # 문자열 -> byte code 변환
        self.client_socket.sendall(data_encoded)  # client socket으로 data 송신
        data = self.client_socket.recv(1024)
        return data.decode()

    def movej(self, joints, rel=False):
        if rel is False:
            msg = 'movej_rel '
            msg += ','.join(str(j) for j in joints)
            self.send(msg)
        else:
            msg = 'movej_abs '
            msg += ','.join(str(j) for j in joints)
            self.send(msg)

    def movel(self, tcp, rel=False):
        if rel is False:
            msg = 'movel_rel '
            msg += ','.join(str(j) for j in tcp)
            self.send(msg)
        else:
            msg = 'movel_abs '
            msg += ','.join(str(j) for j in tcp)
            self.send(msg)

    def getl(self):
        pos = self.send('getl')
        return [int(i) for i in pos.split(',')]

    def getj(self):
        pos = self.send('getj')
        return [int(i) for i in pos.split(',')]

    def open_gripper(self):
        self.send('open_gripper')

    def close_gripper(self):
        self.send('close_gripper')

