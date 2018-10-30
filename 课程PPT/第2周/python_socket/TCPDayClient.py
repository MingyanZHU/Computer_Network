import socket
serverName = '120.79.190.92'
serverPort = 13 # Get DAYTIME service
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while(True):
    message = clientSocket.recv(1024)
    if not message:
        break
    print(message.decode())
# print("断开连接")