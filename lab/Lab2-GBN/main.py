import os
import threading

threading.Thread(target=os.system, args=('python sr_client.py >> sr_client.log', )).start()
threading.Thread(target=os.system, args=('python sr_server.py >> sr_server.log', )).start()
threading.Thread(target=os.system, args=('python gbn_client.py >> gbn_client.log', )).start()
threading.Thread(target=os.system, args=('python gbn_server.py >> gbn_server.log', )).start()
