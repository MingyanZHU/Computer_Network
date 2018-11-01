import threading
import gbn

'''用于测试时的Client端'''
client = gbn.GBNClient()
receive_thread = threading.Thread(target=client.begin_receive).start()
send_thread = threading.Thread(target=client.begin_send).start()
