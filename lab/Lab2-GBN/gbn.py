import socket
import random
import select
import threading

LENGTH_SEQENCE = 8
RECV_WINDOW = 128
SEND_WINDOW = 128

MAX_TIMER = 3

SERVER_PORT_1 = 12138
SERVER_PORT_2 = 12139

CLIENT_PORT_1 = 12140
CLIENT_PORT_2 = 12141

SERVER_IP = '127.0.0.1'
CLIENT_IP = '127.0.0.1'

BUFFER_SIZE = 2048


def make_pkt(next_seq_num, data):
    # next_seq_num = next_seq_num % 256
    pkt_s = str(next_seq_num) + ' ' + str(data)
    return pkt_s.encode()


def make_ack_pkt(ack_num):
    return ('ACK ' + str(ack_num)).encode()


class GBNClient(object):
    def __init__(self):
        self.base = 0
        self.next_seq_num = 0
        self.SEND_WINDOW = SEND_WINDOW
        self.timer = 0
        self.socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_1.bind(('', CLIENT_PORT_1))
        self.socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_2.bind(('', CLIENT_PORT_2))
        self.data_seq = []

    def __send(self):
        while self.next_seq_num < self.base + self.SEND_WINDOW:
            pkt = make_pkt(self.next_seq_num, '')
            if self.next_seq_num == self.base:
                self.timer = 0
            self.socket_1.sendto(pkt, (SERVER_IP, SERVER_PORT_1))
            print("Send", self.next_seq_num)
            self.next_seq_num = self.next_seq_num + 1
            self.data_seq.append(pkt)
            # self.acks_seq.append(0)

    def __timeout(self):
        if self.timer > MAX_TIMER:
            self.timer = 0
            for data in self.data_seq:
                self.socket_1.sendto(data, (SERVER_IP, SERVER_PORT_1))

    def __recv(self):
        readable, writeable, errors = select.select([self.socket_1, ], [], [], 1)
        if len(readable) > 0:
            mgs_byte, address = self.socket_1.recvfrom(BUFFER_SIZE)
            message = mgs_byte.decode()
            if 'ACK' in message:
                messages = message.strip()
                print("Receive", message)
                self.base = int(messages[1]) + 1
                self.data_seq = self.data_seq[self.base:]     # 累计确认
                if self.base == self.next_seq_num:
                    self.timer = -1
                else:
                    self.timer = 0
        else:
            self.timer += 1
            if self.timer > MAX_TIMER:
                self.timer = 0
                for data in self.data_seq:
                    self.socket_1.sendto(data, (SERVER_IP, SERVER_PORT_1))
                    print("Resend", data)

    def begin(self):
        while True:
            while self.next_seq_num < self.base + self.SEND_WINDOW:
                pkt = make_pkt(self.next_seq_num, '')
                if self.next_seq_num == self.base:
                    self.timer = 0
                self.socket_1.sendto(pkt, (SERVER_IP, SERVER_PORT_1))
                print("Send", self.next_seq_num)
                self.next_seq_num = self.next_seq_num + 1 % 256
                self.data_seq.append(pkt)

            readable, writeable, errors = select.select([self.socket_2, ], [], [], 1)
            if len(readable) > 0:
                mgs_byte, address = self.socket_2.recvfrom(BUFFER_SIZE)
                message = mgs_byte.decode()
                if 'ACK' in message:
                    messages = message.split()
                    print("Receive", message)
                    self.base = int(messages[1])
                    # self.data_seq = self.data_seq[self.base:]  # 累计确认
                    if self.base == self.next_seq_num:
                        self.timer = -1
                    else:
                        self.timer = 0
            else:
                self.timer += 1
                if self.timer > MAX_TIMER:
                    self.timer = 0
                    for i in range(self.base, self.next_seq_num):
                        self.socket_1.sendto(self.data_seq[i], (SERVER_IP, SERVER_PORT_1))
                        print("Resend", self.data_seq[i])


class GBNServer(object):
    def __init__(self):
        self.base = 0
        self.expected_seq_num = 0
        self.SEND_WINDOW = SEND_WINDOW
        self.RECV_WINDOW = RECV_WINDOW
        self.timer = 0
        self.socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_1.bind(('', SERVER_PORT_1))
        self.socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_2.bind(('', SERVER_PORT_2))
        self.data_seq = []

    def __recv(self):
        readable, writeable, errors = select.select([self.socket_1, ], [], [], 1)
        if len(readable) > 0:
            mgs_byte, address = self.socket_1.recvfrom(BUFFER_SIZE)
            message = mgs_byte.decode().split()
            if int(message[0]) == self.expected_seq_num:
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_2.sendto(ack_pkt, (CLIENT_IP, CLIENT_PORT_2))
                print("Send ACK", self.expected_seq_num)
                self.expected_seq_num += 1
            else:
                ack_pkt = make_ack_pkt(self.expected_seq_num)
                self.socket_2.sendto(ack_pkt, (CLIENT_IP, CLIENT_PORT_2))
                print("ReSend ACK", self.expected_seq_num)

    def begin(self):
        while True:
            self.__recv()
# TODO 1.全双工实现 去除一对socket实现 (当前见 实验指导书)
# TODO 2.模拟丢包实现
# TODO 3.环形数组实现 即0-255 限制seq的长度


def main():
    client = GBNClient()
    server = GBNServer()
    client_thread = threading.Thread(target=client.begin)
    server_thread = threading.Thread(target=server.begin)
    server_thread.start()
    client_thread.start()


if __name__ == '__main__':
    main()
