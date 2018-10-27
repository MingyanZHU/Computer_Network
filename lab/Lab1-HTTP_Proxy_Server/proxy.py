import socket
import threading
import re
import os
import urllib.parse as urlparse
import requests
import time
import json


class ProxyServer(object):
    """ 对于使用https协议的无法进行处理 """
    def __init__(self):
        self.sever_port = 12138  # 代理服务器的主要端口
        self.server_main_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        # 负责接受连接请求的main socket
        self.server_main_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 使用完立即释放
        self.MAX_LISTEN = 10
        self.server_main_socket.bind(('', self.sever_port))
        self.server_main_socket.listen(self.MAX_LISTEN)  # 最大连接数
        self.HTTP_BUFFER_SIZE = 2048  # HTTP缓存大小
        self.__cache_dir = './cache/'  # cache路径
        self.__make_cache()  # 生成当前的cache路径

    def __make_cache(self):
        if not os.path.exists(self.__cache_dir):
            os.mkdir(self.__cache_dir)

    def filter_web(self, url):
        """ 用于过滤禁用网站 """
        with open('./filter.json', 'r') as f:
            filter_json = json.load(f)
            host_denied = filter_json['host']
            for url_denied in host_denied:
                if url in url_denied:
                    return True
            return False

    def filter_ip(self, ip):
        """ 用于禁用制定IP """
        with open('./filter.json', 'r') as f:
            filter_json = json.load(f)
            ip_denied = filter_json['ip']
            if ip in ip_denied:
                return True
            return False

    def filter_fishing(self, url):
        """ 用于实现钓鱼网站 """
        with open('./filter.json', 'r') as f:
            filter_json = json.load(f)
            fishing = filter_json['fishing']
            for fish in fishing:
                if url in fish:
                    return True
            return False

    def proxy_connect(self, sock, address):
        """ 用于实现代理服务器连接和缓存功能 """
        message = sock.recv(self.HTTP_BUFFER_SIZE).decode(
            'utf-8', 'ignore')  # 以utf-8进行解码 同时忽略二进制文件
        print(message)
        headers = message.split('\r\n')  # 以\r\n将HTTP请求报文的头部进行提取
        request_line = headers[0].strip().split()  # 请求报文的第一行为Request Line
        # 将Request Line的method URL和version 3个部分分开
        if len(request_line) < 1:  # Request Line中可能没有URL
            print("Request Line not contains url!")
            print("Full Request Message:", message)
            sock.close()  # 关闭连接sock
            return
        else:
            url = urlparse.urlparse(
                request_line[1][:-1] if request_line[1][-1] == '/' else request_line[1])  
                # 提取Request Line中的URL 并去除末尾的'/'

        if self.filter_web(url.hostname):  # 如果需要过滤某个网站
            with open('./404.html') as f:
                sock.sendall(f.read().encode())
            sock.close()
            return

        if self.filter_ip(address[0]):  # 如果需要过滤某个IP
            with open('./403.html') as f:
                sock.sendall(f.read().encode())
            sock.close()
            return

        if self.filter_fishing(url.hostname):  # 将需要钓鱼的网站重定向至百度
            sock.sendall(requests.get("https://www.baidu.com").content)
            sock.close()
            return

        cache_path = self.__cache_dir + \
            (url.hostname + url.path).replace('/', '_') # 缓存目录
        flag_modified = False # 默认缓存没有更改
        flag_exists = os.path.exists(cache_path)    # 检测缓存目录是否存在
        out_proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if flag_exists:
            cache_time = os.stat(cache_path).st_mtime   # 获取缓存的时间
            headers = {
                'If-Modified-Since': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(cache_time))}
            response = requests.get(url.geturl(), headers=headers)
            if response.status_code == 304: # 如果返回304 则无需进行重新访问
                print("Read From Cache" + cache_path)
                with open(cache_path, "rb") as f:
                    sock.sendall(f.read())
            else:
                flag_modified = True    # 否则证明缓存已经过时

        if not flag_exists or flag_modified:    # 如果没有缓存或者缓存文件已经发生变化
            print("Attempt to connect", url.geturl())
            out_proxy_sock.connect(
                (url.hostname, url.port if url.port else 80))
            out_proxy_sock.sendall(message.encode())
            temp_file = open(cache_path, 'w')
            while True:
                buff = out_proxy_sock.recv(self.HTTP_BUFFER_SIZE)
                if not buff:
                    temp_file.close()
                    out_proxy_sock.close()
                    break
                temp_file.write(buff.decode('utf8', 'ignore'))
                sock.sendall(buff)
            sock.close()


def main():
    proxy = ProxyServer()
    while True:
        new_sock, address = proxy.server_main_socket.accept()
        # new_sock 用于和源主机进行通信
        print(address)
        threading.Thread(target=proxy.proxy_connect,
                         args=(new_sock, address)).start()


if __name__ == '__main__':
    main()
