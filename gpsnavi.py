#!/usr/bin/python3
'''
Simple navi
keypad 3*4

'''

import socket , time ,math 
from io import StringIO
import RPi.GPIO as GPIO
from datetime import datetime
from keypad import keypad_get
#import os
host = '127.0.0.1' #localhost
port = 52001 #enu
bufsize = 150
wide = 195  #作業機幅cm
ax = 0 ;ay = 0;bx = 1 ;by = -1
_ax = 0;_ay = 0;_bx = 1;_by = 0;_rad = 0
aax = 0;aay = 0;bbx = 0;bby = 0;rrad = 0
base = False
area = 0
c = 0
d = False  #枕3 :False  枕2 ：True
r = [[0,0]]*2
rev = 1
nav = 0
nx = 0;ny = 0;nq = 0
I = '|'
O = ' '
view = False
now = datetime.now()
pointfile = '/home/pi/RTKLIB/rtklog/POINTlog_{0:%Y%m%d%H%M}.pos'.format(now)
menseki  = 0;kyori = 0;menseki_total =0

GPIO.setmode(GPIO.BOARD)

#ポジションレバー
key_u = 19 #19番ピン-GND間にマイクロスイッチを付ける
GPIO.setup(key_u,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#キーパッド
key_y = (37 ,35 ,33 ,31 ) #4行
key_x = (29 ,23 ,21) #3列



#座標取得
def setpoint():
    
    buff = StringIO()
    data = sock.recv(bufsize)
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('\n', '')
    dlist = data.split()
    buff.close()
    if  len(dlist)  <15  :
        print("setpoint re-try")
        setpoint()
    return dlist

#Point Save
def pointsave(nowpoint):
    fileobj = open(pointfile, "a", encoding = "utf-8")
    savepoint = "  ".join(nowpoint)
    fileobj.write(savepoint)
    fileobj.write("\n")
    fileobj.close()
    print("PointSave")


        
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    while True:
        key = keypad_get(*key_x, *key_y)
#main           
        if (key == 0 ):
            nowpoint = setpoint()
            if (base == 0) :
                ax = _ax
                ay = _ay
                bx = _bx
                by = _by
                blf = "A-B"
                rad = _rad
            else :
                ax = aax
                ay = aay
                bx = bbx
                by = bby
                blf = "AA-BB"
                rad = rrad
            try :
                nx = float(nowpoint[2]) #基準点からのXｍ
                ny = float(nowpoint[3]) #基準点からYｍ
                nq = float(nowpoint[5]) #1:FIX 2:Float 5:single

            except :
                print("Set error")

            px = nx - ax
            py = ny - ay
            qx = px*math.cos(-rad)-py*math.sin(-rad) #-rad回転
            qy = px*math.sin(-rad)+py*math.cos(-rad)

            
            if qy < 0 : #右回り
                dist = -qy*100 -c #cm
                turn = -1
            else : #左回り
                dist = qy*100 -c #cm
                turn = 1

            syou = dist// wide
            amari = dist % wide

            if amari > wide/2 :
                nav = -( wide - amari ) #近い
                koutei = syou +1
            else :
                nav = amari #遠い
                koutei = syou

            if (koutei+d) % 2 == 0  : #復路
                rev = -1 *turn
            else :                  #往路
                rev = 1 *turn
            if rev == 1  :  #LINE方向
                revfig = "◀"
            else :
               revfig = "▶" 
            arw =  nav * rev
            level = abs(int (arw / 2))
            w = 13
               
            if  w <= arw  :
                fig = O * w + "▲" + I * w
            elif 2 <= arw  < 20:
                fig = O * w + "▲" + I*level + O *(w -level)
            elif -2 < arw < 2 :
                fig = O * w + "▲"
            elif -20 < arw <= -2:
                fig =O * (w -level) + I * level  + "▲"
            elif arw <= -20:
                fig = I * w + "▲" 
                
#速度計算
            r[1] = r[0]
            r[0] = [qx,qy]
            sx = r[0][0] - r[1][0]
            sy = r[0][1] - r[1][1]
            sz = math.sqrt(math.pow(sx,2) + math.pow(sy,2))
            if sz > 4:#72km/h以上はノーカウント
                sz = 0
            spd = sz * 5  #m/s
#作業面積計算
            if ( GPIO.input( key_u ) == 0 ):
                menseki += sz * wide * 0.01 #m2
                kyori += sz #m
                menseki_total += sz * wide * 0.01 #m2

#表示
            if view == 0  :
                if nq == 1:
                    print("\033[32m%s\033[0m" %fig) #green
                elif nq == 2 :
                    print("\033[33m%s\033[0m" %fig) #yellow
                else :
                    print("\033[31m%s\033[0m" %fig) #red
                print("\033[35m    Nav %+4d cm   工程 %d\033[0m" %(nav,koutei))
                print(" 　LINE %s   %s　c=%d" %(revfig,blf,c)) 
                print(" 　Q = %d  速度%4.1f km/h"  %(nq,spd*3.6))
                print("   作業面積＝%d 距離＝%d" %(menseki,kyori))
                                 
            else :
                if nq == 1 :
                    print("\033[32m%s\033[0m" %fig)
                elif nq == 2 :
                    print("\033[33m%s\033[0m" %fig)
                else :
                    print("\033[31m%s\033[0m" %fig)
            
           
#key入力時

        elif ( key == 1 ):
            setAlist = setpoint()
            try :
                _ax = float(setAlist[2])
                _ay = float(setAlist[3])
                c = 0
                _rad =math.atan2(( _by - _ay ),( _bx - _ax ))
                print("A-PointSet")
                time.sleep(1)
                pointsave(setAlist)
            except :
                print("Set error")
                time.sleep(1)
                
        elif ( key == 2 ):
            setBlist = setpoint()
            try :
                _bx = float(setBlist[2])
                _by = float(setBlist[3])
                _rad =math.atan2(( _by - _ay ),( _bx - _ax ))
                print("B-PointSet")
                time.sleep(1)
                pointsave(setBlist)
            except :
                print("Set error")
                time.sleep(1)
        if ( key == 4 ):
            setAAlist = setpoint()
            try :
                aax = float(setAAlist[2])
                aay = float(setAAlist[3])
                rrad =math.atan2(( bby - aay ),( bbx - aax ))
                print("AA-PointSet")
                time.sleep(1)
                pointsave(setAAlist)
            except :
                print("Set error")
                time.sleep(1)
                
        elif ( key == 5 ):
            setBBlist = setpoint()
            try :
                bbx = float(setBBlist[2])
                bby = float(setBBlist[3])
                rrad =math.atan2(( bby - aay ),( bbx - aax ))
                print("BB-PintSet")
                time.sleep(1)
                pointsave(setBBlist)
            except :
                print("Set error")
                time.sleep(1)                
        elif ( key == 3 ): #0補正
                c =  nav +c   
                print("C-PointSet　%6.2f" %c)
                time.sleep(1)
        elif ( key == 9 ): #Ex 基準線交換
                base = not(base)
                print("基準線を変更しました" )
                time.sleep(1)

        elif ( key == 6 ):
            d = not(d)
            print("マーカー反転")
            time.sleep(2)
#        elif ( key == 8 ): # [#]
#            print("シャットダウン")
#            time.sleep(2)
#            os.system("sudo shutdown -h now")
#        elif ( key == 10 ): 
#            print("再起動")
#            time.sleep(2)
#            os.system("sudo reboot")
#        elif ( key == 12):#総面積リセット
#            menseki_total = 0
#            print("総面積リセット")
#            time.sleep(2)      

        elif ( key == 7): #表示切り替え
            view = not(view)
            time.sleep(1)
        elif ( key == 8):#PointSave
            pointsave(setpoint())
            print("PointSave")
            time.sleep(1)
        elif ( key == 11):#面積リセット
            menseki = 0
            print("作業面積リセット")
            time.sleep(2)
        elif ( key == 10):#距離リセット
            kyori = 0
            print("走行距離リセット")
            time.sleep(2)
        
except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
GPIO.cleanup()