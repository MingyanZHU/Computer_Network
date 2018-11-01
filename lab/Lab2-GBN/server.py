import threading
import gbn

'''用于测试时Server端'''
server = gbn.GBNServer()
receive_thread = threading.Thread(target=server.begin_receive).start()
send_thread = threading.Thread(target=server.begin_send).start()
