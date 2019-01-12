import socket
import datetime
import threading

serverPort = 13
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print("The server is ready to receive:")

def tcpGetTime(newSock, addr):
    print("client address:", addr)
    newSock.send("Welcome to connect to ZMY aliyun server to get time")
    newSock.send(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S').encode())
    newSock.close()

while True:
    newSock, addr = serverSocket.accept()
    newThread = threading.Thread(target=tcpGetTime, args=(newSock, addr))
    newThread.start()
    
    
