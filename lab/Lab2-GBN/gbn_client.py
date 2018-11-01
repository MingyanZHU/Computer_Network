import threading
import gbn

'''用于测试时的GBN Client端'''

client_gbn = gbn.GBNClient()
receive_thread_gbn = threading.Thread(target=client_gbn.begin_receive)
send_thread_gbn = threading.Thread(target=client_gbn.begin_send)
receive_thread_gbn.start()
send_thread_gbn.start()
