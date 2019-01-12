import socket
serverName = '120.79.190.92'
# 阿里云服务器的ip地址
serverPort = 13 
# Get DAYTIME service
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#建立TCP连接
clientSocket.connect((serverName, serverPort))

while(True):
    message = clientSocket.recv(1024)
    if not message:
        break
    print(message.decode())
# print("断开连接")