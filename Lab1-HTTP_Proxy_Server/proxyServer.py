import socket
import threading
import re
import os
import urllib.parse as urlp

class ProxyServer:
    def __init__(self):
        self.serverPort = 12138
        self.serverMainSocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.serverMainSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverMainSocket.bind(('', self.serverPort))
        self.serverMainSocket.listen(10)
        self.HTTP_BUFFER_SIZE = 4096

    def tcpGetConnect(self, newSock, addr):
        message = newSock.recv(self.HTTP_BUFFER_SIZE).decode()
        megs = message.split("\r\n") # 按照"\r\n"将请求消息的首部拆分为列表
        request_line = megs[0].strip().split() # 请求消息第一行为Request Line
        # 将Request Line的method、URL和version 3个部分拆开
        new_out_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        url = urlp.urlparse(request_line[1])
        out_host = url.hostname # 使用urllib获取url中的host
        print("尝试连接:", url.hostname+url.path)
        # 利用新的向外连接的socket对目标主机进行访问
        new_out_Socket.connect((out_host, 80))
        new_out_Socket.sendall(message.encode())
        while True:
            buff = new_out_Socket.recv(self.HTTP_BUFFER_SIZE)
            if not buff:
                new_out_Socket.close()
                break
            newSock.sendall(buff)
        # TODO 实现缓存功能 以及扩展功能
        # # GET http://www.hit.edu.cn HTTP/1.1
        # find = re.match(pattern, message.spilt()[1])
        # if find:
        #     fileName = find.group(2).replace("/", "_")
        # else :
        #     print("Error")
        # fileExist = False
        # try :
        #     f = open(fileName, "r")
        #     output = f.readlines()
        #     fileExist = True
        #     for i in range(len(output)):
        #         newSock.send(output[i].encode())
        # except IOError:
        #     print("File exist:", fileExist)
        #     newOutSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     hostn = message.split()[1].partition("//")[2].partition("/")[0]
        #     newOutSock.connect((hostn, 80))
        #     newOutSock.sendall(message.encode())
        #     while True:
        #         buff = newOutSock.recv(self.HTTP_BUFFER_SIZE)
        #         if not buff:
        #             break
        #         newSock.sendall(buff)


def main():
    proxy = ProxyServer()
    while True:
        print("Proxy server is ready to receive message:")
        newSock, addr = proxy.serverMainSocket.accept()
        newThread = threading.Thread(
            target=proxy.tcpGetConnect, args=(newSock, addr))
        print("Thread name:", newThread, "client address:", addr)
        newThread.start()


if __name__ == '__main__':
    main()
