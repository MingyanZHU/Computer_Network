import socket
# serverName = '120.79.190.92'
serverName = '127.0.0.1'
# 阿里云服务器的ip地址
serverPort = 12138 
# Get DAYTIME service
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#建立TCP连接
clientSocket.connect((serverName, serverPort))
string = "GET http://www.bit.edu.cn HTTP/1.1\r\nHost: www.bit.edu.cn\r\nProxy-Connection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36\r\n\r\n"

while True:
    s = input("Input something:")
    if s == "E":
        break
    else :
        clientSocket.send(string.encode())
        while True:
            message = clientSocket.recv(1024)
            if not message:
                break
            print(message.decode())