import threading
import gbn

'''用于测试时的GBN Server端'''
server_gbn = gbn.GBNServer()
receive_thread_gbn = threading.Thread(target=server_gbn.begin_receive)
send_thread_gbn = threading.Thread(target=server_gbn.begin_send)
receive_thread_gbn.start()
send_thread_gbn.start()
