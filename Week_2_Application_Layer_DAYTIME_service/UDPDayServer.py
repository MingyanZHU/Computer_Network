import socket
import datetime
serverPort = 13
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server in ready to recevie")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    serverSocket.sendto(datetime.datetime.now(), clientAddress)