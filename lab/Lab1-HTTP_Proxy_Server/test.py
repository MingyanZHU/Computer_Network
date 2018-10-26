# meg = "111 3333 4444 \r\n222\r\n"
# mgs = meg.split("\r\n")
# print(mgs)

# urltest = "https://docs.python.org/2/library/urlparse.html"
# import urllib.parse
# url = urllib.parse.urlparse(urltest)
# print(url)
# host = url.hostname
# file_name = (url.hostname + url.path).replace('/', '_')
# print(file_name)
# print(host)
# print(url.path)
# print(not url.port)
# print(url.port if url.port else 80)
import os
import time
import requests
file_time = os.stat("/home/zmy/data/Computer_Network/lab/Lab1-HTTP_Proxy_Server/proxyServer.py").st_mtime
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Content-Type": "application/ocsp-request",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
'If-Modified-Since': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time()))}

s = requests.Session()
# s.headers.update(headers)
print(s.headers)
print(s)
# print(requests.get("http://www.fudan.edu.cn/"))
# re = s.get("http://en.wikipedia.org/wiki/Main_Page")
re = s.get("http://www.baidu.com/")
print(re.status_code)
print(re.headers['content-type'])
print(re.encoding)
print(re.content.decode(re.encoding))

# import socket
# import time
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("www.hit.edu.cn", 80))
# if_modified = "If-Modified-Since: " + str(time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time()))) + "\r\n"
# # message = "GET http://www.bit.edu.cn/ HTTP/1.1\r\nHost: www.bit.edu.cn\r\n"+"\r\n"
# message = "GET http://www.bit.edu.cn/ HTTP/1.1\r\nHost: www.bit.edu.cn\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n" + if_modified + "\r\n"
# print(message)
# sock.sendall(message.encode())
# buff = sock.recv(4096)
# print(buff)
# re = s.get("http://www.huaxiaozhuan.com")
# print(re.status_code)
# print(re.headers)

# print(requests.get('http://home/zmy/data/Computer_Network/lab/Lab1-HTTP_Proxy_Server/301.html').content)

# r = requests.get('http://en.wikipedia.org/wiki/Monty_Python', headers=headers)
# print(r.status_code)
# print(r.request.headers)
# print(re.headers['If-Modified-Since'])
# print(re.content)
# print(headers)

# import json
# with open('./filter.json', 'r') as f:
#     filter_json = json.load(f)
#     for fish in filter_json['fishing']:
#         print(fish)
#     print(filter_json['fishing'])
# begin = time.time()
# with open('./cache/jwts.hit.edu.cn_', 'r') as f:
#     print(f.read())
# end_time = time.time()
# print(end_time - begin)

# begin = time.time()
# with open('./cache/jwts.hit.edu.cn_', 'r') as f:
#     output = f.readlines()
#     for i in range(len(output)):
#         print(output[i])
# end_time = time.time()
# print(end_time - begin)
""" 重构代码 """
# # TODO 此处暂时只考虑了GET方法
# send = requests.Session()
# request_headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"}
# send.headers.update(request_headers)
# print("Connect", url.geturl())
# respose = send.get(url.geturl())
# if respose.status_code == 200:
#     sock.sendall(respose.content)
#     # sock.sendall(respose.text.encode(respose.encoding, 'ignore'))
# sock.close()

# import urllib.parse as urlparse
# url = urlparse.urlparse("http://www.fudan.edu.cn/")
# print(url)
