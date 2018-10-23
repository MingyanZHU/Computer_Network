import socket
import threading
import re
import os
import urllib.parse as urlp
import requests
import time

class ProxyServer:
    def __init__(self):
        self.serverPort = 12138
        self.serverMainSocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.serverMainSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverMainSocket.bind(('', self.serverPort))
        self.serverMainSocket.listen(10)
        self.HTTP_BUFFER_SIZE = 4096
        self.__cache_dir = './cache/'
        self.__make_cache()

    def __make_cache(self):
        if not os.path.exists(self.__cache_dir):
            os.mkdir(self.__cache_dir)

    def tcpGetConnect(self, newSock, addr):
        message = newSock.recv(self.HTTP_BUFFER_SIZE).decode("utf8","ignore")
        megs = message.split("\r\n") # 按照"\r\n"将请求消息的首部拆分为列表
        request_line = megs[0].strip().split() # 请求消息第一行为Request Line
        # 将Request Line的method、URL和version 3个部分拆开
        new_out_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if len(request_line) < 1:
            print(request_line)
            new_out_Socket.close()
            return
        else :
            url = urlp.urlparse(request_line[1])
        file_name = self.__cache_dir + (url.hostname + url.path).replace('/', '_')
        flag_modified = False
        flag_exists = os.path.exists(file_name)
        if flag_exists:
            # 检查是否有缓存文件
            # 检查是否过期
            # TODO cache 待完善 做的很糙
            # TODO 钓鱼网站的实现
            file_time = os.stat(file_name).st_mtime
            headers = {'If-Modified-Since': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(file_time))}
            send = requests.Session()
            send.headers.update(headers)
            re = send.get(url.geturl())
            if re.status_code == 304:
                print("Read from cache: " + file_name)
                with open(file_name, "r") as f:
                    # for line in f:
                    #     newSock.send(line.encode())
                    # 莫名很慢 有时候甚至读不出来
                    output = f.readlines()
                    for i in range(len(output)):
                        newSock.send(output[i].encode())
            else :
                os.remove(file_name)
                flag_modified = True
        if not flag_exists or flag_modified :
            out_host = url.hostname # 使用urllib获取url中的host
            print("尝试连接:", url.geturl())
            # 利用新的向外连接的socket对目标主机进行访问
            new_out_Socket.connect((out_host, 80))
            new_out_Socket.sendall(message.encode())
            temp_file = open(file_name, "w")
            while True:
                buff = new_out_Socket.recv(self.HTTP_BUFFER_SIZE)
                if not buff:
                    temp_file.close()
                    # new_out_Socket.close()
                    break
                temp_file.writelines(buff.decode("utf8","ignore"))
                newSock.sendall(buff)


def main():
    proxy = ProxyServer()
    while True:
        # print("Proxy server is ready to receive message:")
        newSock, addr = proxy.serverMainSocket.accept()
        newThread = threading.Thread(
            target=proxy.tcpGetConnect, args=(newSock, addr))
        # print("Thread name:", newThread, "client address:", addr)
        newThread.start()


if __name__ == '__main__':
    main()
