import threading
import sr

'''用于测试时的SR Client端'''
client_sr = sr.SRClient()
receive_thread_sr = threading.Thread(target=client_sr.begin_receive)
send_thread_sr = threading.Thread(target=client_sr.begin_send)
receive_thread_sr.start()
send_thread_sr.start()
