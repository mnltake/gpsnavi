#!/usr/bin/python3
import socket ,os,time
from datetime import datetime
host = '127.0.0.1' #localhost
port = 52002
bufsize = 150
time.sleep(60)
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    now = datetime.now()
    folder  = './log/TGSlog_{0:%Y%m}/'.format(now)
    file = '{0:%d%H%M}.pos'.format(now)
    while True:
        if not os.path.exists(folder):
            os.makedirs(folder)
        fileobj = open(folder + file, "a", encoding = "utf-8")
        savepoint = sock.recv(bufsize)
        print(savepoint)
        fileobj.write(savepoint.decode('utf-8'))
        fileobj.close()
        print("PointSave")
except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
