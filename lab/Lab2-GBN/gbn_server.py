import socket
import datetime
serverPort = 12138
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server in ready to recevie")
while True:
    megs_bytes, clientAddress = serverSocket.recvfrom(2048)
    message = megs_bytes.decode()
    if message in ("-t", "--time"):
        serverSocket.sendto(str(datetime.datetime.now()).encode(), clientAddress)
    elif message in ("-q", "--quit"):
        serverSocket.close()
        break
    elif message in ("-e", "--testgbn"):
        print("Test GBN")
    else:
        serverSocket.sendto(message.encode(), clientAddress)