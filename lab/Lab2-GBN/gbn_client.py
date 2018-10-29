import socket
import sys
import getopt


class Client(object):
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 12138
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.BUFF_SIZE = 2048

    def start(self, argv):
        try:
            opts, args = getopt.getopt(argv, "htqe", ["help", "time", "quit", "testgbn"])
        except getopt.GetoptError:
            print("gbn_client.py --help or -h for help")
            self.client_socket.close()
            sys.exit(2)
        # print(opts)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print("Using \" gbn_client.py -t or --time\" to get the server time")
                print("Using \" gbn_client.py -e or --testgbn\" to begin GBN testing state")
                print("Using \" gbn_client.py -q or --quit\" to quit")
            elif opt in ("-t", "--time"):
                self.client_socket.sendto(opt.encode(), (self.server_ip, self.server_port))
                server_time, server_address = self.client_socket.recvfrom(self.BUFF_SIZE)
                print("Server " + str(server_address) +" Time:" , server_time.decode())
            elif opt in ("-e", "--testgbn"):
                print("Test GBN")
            elif opt in ("-q", "--quit"):
                self.client_socket.close()
                print("Quit")
                break
            else:
                print("gbn_client.py --help or -h for help")
                self.client_socket.sendto(opt.encode(), (self.server_ip, self.server_port))
                server_message, server_address = self.client_socket.recvfrom(self.BUFF_SIZE)
                print("Server " + str(server_address), server_message.decode())
        


def main(argv):
    client = Client()
    # print(argv)
    while True:
        client.start(argv)
        message = input()
        argv = [message]
        if message == '-q' or message == '--quit':
            client.start(argv)
            break

if __name__ == '__main__':
    main(sys.argv[1:])