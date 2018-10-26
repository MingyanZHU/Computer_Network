import socket
import threading
import re
import os
import urllib.parse as urlp
import requests
import time
import json


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

    def filter_web(self, url):
        with open('./filter.json', 'r') as f:
            filter_json = json.load(f)
            host_denied = filter_json['host']
            for url_denied in host_denied:
                if url in url_denied:
                    return True
            return False

    def filter_fishing(self, url):
        with open('./filter.json', 'r') as f:
            filter_json = json.load(f)
            fishing = filter_json['fishing']
            for fish in fishing:
                if url in fish:
                    with open('./301_move.txt') as f:
                        return f.read()
                    #　TODO 不能显示的原因404 not found 在于 没有后加HTML
                    #　TODO 可以根据test.py中 获取某种404反馈 
        return False

    def tcp_get_connect(self, new_sock):
        message = new_sock.recv(self.HTTP_BUFFER_SIZE).decode("utf8", "ignore")
        megs = message.split("\r\n")  # 按照"\r\n"将请求消息的首部拆分为列表
        request_line = megs[0].strip().split()  # 请求消息第一行为Request Line
        # 将Request Line的method、URL和version 3个部分拆开
        if len(request_line) < 1:
            print("请求行中不包含URL")
            print(message)
            print(request_line)
            return
        else:
            url = urlp.urlparse(request_line[1])
        if self.filter_web(url.hostname):
            print("Denied ", url.geturl())
            with open('./404.html') as f:
                new_sock.sendall(f.read().encode())
            new_sock.close()
            return
        fish = self.filter_fishing(url.hostname)
        if fish:
            print("www.fudan.edu.cn")
            new_sock.send(requests.get('http://www.zju.edu.cn').content)
            # TODO 完善钓鱼和限制网站
            return 
        new_out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            response = send.get(url.geturl())
            if response.status_code == 304:
                print("Read from cache: " + file_name)
                with open(file_name, "r") as f:
                    # for line in f:
                    #     new_sock.send(line.encode())
                    # 莫名很慢 有时候甚至读不出来
                    # output = f.readlines()
                    # for i in range(len(output)):
                    #     new_sock.sendall(output[i].encode())
                    new_sock.sendall(f.read().encode())
            else:
                os.remove(file_name)
                flag_modified = True
        if not flag_exists or flag_modified:
            out_host = url.hostname  # 使用urllib获取url中的host
            print("尝试连接:", url.geturl())
            # 利用新的向外连接的socket对目标主机进行访问
            new_out_socket.connect((out_host, 80))
            new_out_socket.sendall(message.encode())
            temp_file = open(file_name, "w")
            while True:
                buff = new_out_socket.recv(self.HTTP_BUFFER_SIZE)
                if not buff:
                    temp_file.close()
                    new_out_socket.close()
                    break
                temp_file.writelines(buff.decode("utf8", "ignore"))
                new_sock.sendall(buff)


def main():
    proxy = ProxyServer()
    while True:
        # print("Proxy server is ready to receive message:")
        new_sock, address = proxy.serverMainSocket.accept()
        print(address)
        threading.Thread(target=proxy.tcp_get_connect, args=(new_sock,)).start()


if __name__ == '__main__':
    main()
