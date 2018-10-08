import socket
import threading
import re
import os

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
        # GET http://www.hit.edu.cn HTTP/1.1
        pattern = '(https?|ftp|file)://([-A-Za-z0-9+&@#/%?=~_|!:,.;]+)[-A-Za-z0-9+&@#/%=~_|]'
        find = re.match(pattern, message.spilt()[1])
        if find:
            fileName = find.group(2).replace("/", "_")
        else :
            print("Error")
        fileExist = False
        try :
            f = open(fileName, "r")
            output = f.readlines()
            fileExist = True
            for i in range(len(output)):
                newSock.send(output[i].encode())
        except IOError:
            print("File exist:", fileExist)
            newOutSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hostn = message.split()[1].partition("//")[2].partition("/")[0]
            newOutSock.connect((hostn, 80))
            newOutSock.sendall(message.encode())
            while True:
                buff = newOutSock.recv(self.HTTP_BUFFER_SIZE)
                if not buff:
                    break
                newSock.sendall(buff)


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
