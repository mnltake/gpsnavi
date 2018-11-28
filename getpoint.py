#!/usr/bin/python3
import socket 
from io import StringIO

#座標取得
def getpoint():
    
    buff = StringIO()
    data = sock.recv(bufsize)
    #print(data)
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
