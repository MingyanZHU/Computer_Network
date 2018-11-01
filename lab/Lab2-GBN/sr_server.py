import threading
import sr


'''用于测试时SR Server端'''
server_sr = sr.SRServer()
receive_thread_sr = threading.Thread(target=server_sr.begin_receive)
send_thread_sr = threading.Thread(target=server_sr.begin_send)
receive_thread_sr.start()
send_thread_sr.start()

