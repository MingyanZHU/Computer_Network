import socket
import random
import select
import threading
import time

LENGTH_SEQUENCE = 256  # 序列号有效范围 0~255
RECEIVE_WINDOW = 128  # 接收窗口大小(SR协议中使用)
SEND_WINDOW = 5  # 发送窗口大小

MAX_TIMER = 3  # 计时器最大超时时间

SERVER_PORT_1 = 12138
SERVER_PORT_2 = 12139

CLIENT_PORT_1 = 12140
CLIENT_PORT_2 = 12141

SERVER_IP = '127.0.0.1'
CLIENT_IP = '127.0.0.1'

BUFFER_SIZE = 2048  # 缓存大小


def make_pkt(next_seq_num, data):
    """数据帧格式
     SEQ' 'data
     """
    pkt_s = str(next_seq_num) + ' ' + str(data)
    return pkt_s.encode()


def make_ack_pkt(ack_num):
    """ACK帧格式
    ACK' 'ack_num
    """
    return ('ACK ' + str(ack_num)).encode()


class GBNClient(object):
    def __init__(self):
        self.base = 0
        self.next_seq_num = 0
        self.expected_seq_num = 0
        self.SEND_WINDOW = SEND_WINDOW
        self.timer = 0
        self.socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 主要用作Client作为发送端的socket
        self.socket_1.bind(('', CLIENT_PORT_1))
        self.socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 主要用作Client作为接收端的socket
        self.socket_2.bind(('', CLIENT_PORT_2))
        self.data_send_seq = [b'0'] * LENGTH_SEQUENCE  # 作为已发送数据的缓存
        self.data_receive_seq = [0] * LENGTH_SEQUENCE   # 作为接受数据的缓存

    def __timeout(self):
        print("Client Timer Timeout")
        self.timer = 0
        for i in range(self.base,
                       self.next_seq_num if self.next_seq_num > self.base
                       else self.next_seq_num + LENGTH_SEQUENCE):
            # 用于序列号使用的处理
            self.socket_1.sendto(self.data_send_seq[i % LENGTH_SEQUENCE], (SERVER_IP, SERVER_PORT_1))
            print("Client Resend", self.data_send_seq[i % LENGTH_SEQUENCE])

    def __send(self):
            while self.next_seq_num <= (self.base + self.SEND_WINDOW) % LENGTH_SEQUENCE:
                pkt = make_pkt(self.next_seq_num, str(self.next_seq_num + LENGTH_SEQUENCE))
                if self.next_seq_num == self.base:
                    self.timer = 0
                self.socket_1.sendto(pkt, (SERVER_IP, SERVER_PORT_1))
                print("Client Send", self.next_seq_num)
                self.data_send_seq[self.next_seq_num] = pkt
                self.next_seq_num = self.next_seq_num + 1

            self.next_seq_num = self.next_seq_num % LENGTH_SEQUENCE
            readable, writeable, errors = select.select([self.socket_1, ], [], [], 1)
            # 非阻塞方式
            if len(readable) > 0:
                mgs_byte, address = self.socket_1.recvfrom(BUFFER_SIZE)
                message = mgs_byte.decode()
                if 'ACK' in message:
                    messages = message.split()
                    print("Client Receive", message)
                    self.base = (int(messages[1]) + 1) % LENGTH_SEQUENCE
                    if self.base == self.next_seq_num:
                        self.timer = -1
                    else:
                        self.timer = 0
            else:
                # 如果没有收到ACK 则将定时器加1
                self.timer += 1
                if self.timer > MAX_TIMER:
                    self.__timeout()

    def begin_send(self):
        while True:
            self.__send()

    def __receive(self):
        time.sleep(random.random())  # 用于测试时观察 模拟网络延迟
        readable, writeable, errors = select.select([self.socket_2, ], [], [], 1)
        if len(readable) > 0:
            mgs_byte, address = self.socket_2.recvfrom(BUFFER_SIZE)
            message = mgs_byte.decode().split()
            if int(message[0]) == self.expected_seq_num:
                self.data_receive_seq[self.expected_seq_num] = message[1]
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_2.sendto(ack_pkt, (SERVER_IP, SERVER_PORT_2))
                print("Client Send ACK", self.expected_seq_num)
                self.expected_seq_num = (self.expected_seq_num + 1) % LENGTH_SEQUENCE
            else:
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_2.sendto(ack_pkt, (SERVER_IP, SERVER_PORT_2))
                print("Client Resend ACK", self.expected_seq_num)

    def __receive_random_throw(self):
        time.sleep(random.random())  # 用于测试时观察 模拟网络延迟
        readable, writeable, errors = select.select([self.socket_2, ], [], [], 1)
        if len(readable) > 0:
            mgs_byte, address = self.socket_2.recvfrom(BUFFER_SIZE)
            message = mgs_byte.decode().split()
            if int(message[0]) == self.expected_seq_num:
                self.data_receive_seq[self.expected_seq_num] = message[1]
                time.sleep(random.uniform(0, 3))    # 制造延迟 模拟Timer超时
                if random.getrandbits(1) == 0:  # 50%概率发送ACK报文
                    ack_pkt = make_ack_pkt(self.expected_seq_num)
                    self.socket_2.sendto(ack_pkt, (SERVER_IP, SERVER_PORT_2))
                    print("Client Send ACK", self.expected_seq_num)

                self.expected_seq_num = (self.expected_seq_num + 1) % LENGTH_SEQUENCE
            else:
                print("Client don't expect", message)
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_2.sendto(ack_pkt, (SERVER_IP, SERVER_PORT_2))
                print("Client Resend ACK", self.expected_seq_num)

    def begin_receive(self):
        while True:
            # self.__receive()
            self.__receive_random_throw()  # 用作随机丢包测试


class GBNServer(object):
    def __init__(self):
        self.base = 0
        self.expected_seq_num = 0
        self.next_seq_num = 0
        self.SEND_WINDOW = SEND_WINDOW
        # self.RECEIVE_WINDOW = RECEIVE_WINDOW
        # 暂未使用 GBN协议中作为接收端的接收窗口大小为1
        self.timer = 0
        self.socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 主要用作Server作为接收端的socket
        self.socket_1.bind(('', SERVER_PORT_1))
        self.socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 主要用作Server作为发送端的socket
        self.socket_2.bind(('', SERVER_PORT_2))
        self.data_receive_seq = [b'0'] * LENGTH_SEQUENCE  # 接收数据的缓存
        self.data_send_seq = [b'0'] * LENGTH_SEQUENCE   # 作为发送数据的缓存

    def __receive(self):
        time.sleep(random.random())  # 用于测试时观察 模拟网络延迟
        readable, writeable, errors = select.select([self.socket_1, ], [], [], 1)
        if len(readable) > 0:
            mgs_byte, address = self.socket_1.recvfrom(BUFFER_SIZE)
            message = mgs_byte.decode().split()
            if int(message[0]) == self.expected_seq_num:
                self.data_receive_seq[self.expected_seq_num] = message[1]
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_1.sendto(ack_pkt, (CLIENT_IP, CLIENT_PORT_1))
                print("Server Send ACK", self.expected_seq_num)
                self.expected_seq_num = (self.expected_seq_num + 1) % LENGTH_SEQUENCE
            else:
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_1.sendto(ack_pkt, (CLIENT_IP, CLIENT_PORT_1))
                print("Server Resend ACK", self.expected_seq_num)

    def __receive_random_throw(self):
        time.sleep(random.random())  # 用于测试时观察 模拟网络延迟
        readable, writeable, errors = select.select([self.socket_1, ], [], [], 1)
        if len(readable) > 0:
            mgs_byte, address = self.socket_1.recvfrom(BUFFER_SIZE)
            message = mgs_byte.decode().split()
            if int(message[0]) == self.expected_seq_num:
                self.data_receive_seq[self.expected_seq_num] = message[1]
                time.sleep(random.uniform(0, 3))    # 制造延迟 模拟Timer超时
                if random.getrandbits(1) == 0:  # 50%概率发送ACK报文
                    ack_pkt = make_ack_pkt(self.expected_seq_num)
                    self.socket_1.sendto(ack_pkt, (CLIENT_IP, CLIENT_PORT_1))
                    print("Server Send ACK", self.expected_seq_num)

                self.expected_seq_num = (self.expected_seq_num + 1) % LENGTH_SEQUENCE
            else:
                print("Server don't expect", message)
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_1.sendto(ack_pkt, (CLIENT_IP, CLIENT_PORT_1))
                print("Server Resend ACK", self.expected_seq_num)

    def begin_receive(self):
        while True:
            # self.__receive()
            self.__receive_random_throw()  # 用作随机丢包测试

    def __timeout(self):
        print("Server Timer Timeout")
        self.timer = 0
        for i in range(self.base,
                       self.next_seq_num if self.next_seq_num > self.base
                       else self.next_seq_num + LENGTH_SEQUENCE):
            # 用于序列号使用的处理
            self.socket_2.sendto(self.data_send_seq[i % LENGTH_SEQUENCE], (CLIENT_IP, CLIENT_PORT_2))
            print("Server Resend", self.data_send_seq[i % LENGTH_SEQUENCE])

    def __send(self):
            while self.next_seq_num <= (self.base + self.SEND_WINDOW) % LENGTH_SEQUENCE:
                pkt = make_pkt(self.next_seq_num, str(self.next_seq_num + LENGTH_SEQUENCE))
                if self.next_seq_num == self.base:
                    self.timer = 0
                self.socket_2.sendto(pkt, (CLIENT_IP, CLIENT_PORT_2))
                print("Server Send", self.next_seq_num)
                self.data_send_seq[self.next_seq_num] = pkt
                self.next_seq_num = self.next_seq_num + 1

            self.next_seq_num = self.next_seq_num % LENGTH_SEQUENCE
            readable, writeable, errors = select.select([self.socket_2, ], [], [], 1)
            # 非阻塞方式
            if len(readable) > 0:
                mgs_byte, address = self.socket_2.recvfrom(BUFFER_SIZE)
                message = mgs_byte.decode()
                if 'ACK' in message:
                    messages = message.split()
                    print("Server Receive", message)
                    self.base = (int(messages[1]) + 1) % LENGTH_SEQUENCE
                    if self.base == self.next_seq_num:
                        self.timer = -1
                    else:
                        self.timer = 0
            else:
                # 如果没有收到ACK 则将定时器加1
                self.timer += 1
                if self.timer > MAX_TIMER:
                    self.__timeout()

    def begin_send(self):
        while True:
            self.__send()


def main():
    client = GBNClient()
    server = GBNServer()
    client_receive_thread = threading.Thread(target=client.begin_receive)
    server_send_thread = threading.Thread(target=server.begin_send)
    client_receive_thread.start()
    server_send_thread.start()
    client_send_thread = threading.Thread(target=client.begin_send)
    server_receive_thread = threading.Thread(target=server.begin_receive)
    server_receive_thread.start()
    client_send_thread.start()


if __name__ == '__main__':
    main()
