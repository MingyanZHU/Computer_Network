import os
import threading

threading.Thread(target=os.system, args=('python client.py >> client.log', )).start()
threading.Thread(target=os.system, args=('python server.py >> server.log', )).start()
