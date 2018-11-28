#!/usr/bin/python3
import socket 
from io import StringIO
from datetime import datetime
#host = '127.0.0.1' #localhost
host = '192.168.3.20' 
port = 52002
bufsize = 256
buff = StringIO()
filepath = '/home/pi/rtklog/'
#filepath = 'H:/rtklog/'
#座標取得
def getpoint():
    
    buff = StringIO()
    data = sock.recv(bufsize)
    #print(len(data))
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('\n', '')
    dlist = data.split()
    #print(dlist)
    #print(len(dlist))
    buff.close()
    if  len(dlist)  <15  :
        print("getpoint re-try")
        getpoint()
    return dlist

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    now = datetime.now()
    file = 'TGSlog_{0:%Y%m%d%H%M}.csv'.format(now)
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
