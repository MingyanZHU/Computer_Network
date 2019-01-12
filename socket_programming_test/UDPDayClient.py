import socket
serverName = '120.79.190.92'
serverPort = 13 # Get DAYTIME service
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Get time".encode()
# 将信息编码为bytes格式以便于发送
clientSocket.sendto(message, (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
