#!/usr/bin/python3
import socket 
from io import StringIO
from datetime import datetime
port = 52002
bufsize = 150
buff = StringIO()
filepath = '../rtklog/'
#座標取得
def getpoint():
    buff = StringIO()
    data = sock.recv(bufsize)
    print(data)
    buff.write(data.decode('utf-8'))
    data = buff.getvalue()
    dlist = data.split()
    #print(dlist)
    #print(len(dlist))
    buff.close()
    return dlist

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    now = datetime.now()
    file = 'TGSlog_{0:%Y%m%d%H%M}.pos'.format(now)
    while True:
        fileobj = open(filepath + file, "a", encoding = "utf-8")
        savepoint = " ".join(getpoint())
        fileobj.write(savepoint + "\n")
        fileobj.close()
        print("PointSave")
except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
