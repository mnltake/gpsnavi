#!/usr/bin/python3
import socket , time ,math ,os
from io import StringIO
import RPi.GPIO as GPIO

host = '127.0.0.1' #localhost
port = 52001
#host = '192.168.3.6' #tab
#port = 52004
bufsize = 200
buff = StringIO()
wide = 195  #作業機幅cm
_ax = 0
_ay = 0
_bx = 1
_by = 0
ax = 0
ay = 0
bx = 1
by = 0
aax = 0
aay = 0
bbx = 0
bby = 1
c = 0
d = 0  #枕3 :0  枕2 ：1
base = 0
r = [[0,0]]*5
rev = 1
nav = 0
nx = 0
ny = 0
nq = 0
I = '|'
O = ' '
view = 0
#キーパッド
GPIO.setmode(GPIO.BCM)
key_x = [13 ,19 ,26 ]
key_y = [9 ,11 ,5 , 6]
GPIO.setup(key_y,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(key_x,GPIO.OUT)
def keypad_get():
    GPIO.output(key_x[0], GPIO.LOW )
    GPIO.output(key_x[1], GPIO.HIGH )
    GPIO.output(key_x[2], GPIO.HIGH )
    if ( GPIO.input(key_y[0]) == 0 ):
        return 1
    elif ( GPIO.input(key_y[1]) == 0 ):
        return 4
    elif ( GPIO.input(key_y[2]) == 0 ):
        return 7
    elif ( GPIO.input(key_y[3]) == 0 ):
        return 11  # [*]

    GPIO.output(key_x[0], GPIO.HIGH )
    GPIO.output(key_x[1], GPIO.LOW )
    GPIO.output(key_x[2], GPIO.HIGH )
    if ( GPIO.input(key_y[0]) == 0 ):
        return 2
    elif ( GPIO.input(key_y[1]) == 0 ):
        return 5
    elif ( GPIO.input(key_y[2]) == 0 ):
        return 8
    elif ( GPIO.input(key_y[3]) == 0 ):
        return 0

    GPIO.output(key_x[0], GPIO.HIGH )
    GPIO.output(key_x[1], GPIO.HIGH )
    GPIO.output(key_x[2], GPIO.LOW )
    if ( GPIO.input(key_y[0]) == 0 ):
        return 3
    elif ( GPIO.input(key_y[1]) == 0 ):
        return 6
    elif ( GPIO.input(key_y[2]) == 0 ):
        return 9
    elif ( GPIO.input(key_y[3]) == 0 ):
        return 12 # [#]

    return
#座標取得
def setpoint():
    buff = StringIO()
    data = sock.recv(bufsize)
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('> ', '>\n ')
    dlist = data.split()
    buff.close()
    return dlist

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    while True:
        key = keypad_get()
        if ( key == 2 ):
            setAlist = setpoint()
            try :
                _ax = float(setAlist[2])
                _ay = float(setAlist[3])
                c = 0
                print("A-PointSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)
                
        elif ( key == 5 ):
            setBlist = setpoint()
            try :
                _bx = float(setBlist[2])
                _by = float(setBlist[3])
                print("B-PintSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)
        if ( key == 1 ):
            setAAlist = setpoint()
            try :
                aax = float(setAAlist[2])
                aay = float(setAAlist[3])
                print("AA-PointSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)
                
        elif ( key == 4 ):
            setBBlist = setpoint()
            try :
                bbx = float(setBBlist[2])
                bby = float(setBBlist[3])
                print("BB-PintSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)                
        elif ( key == 8 ): #0補正
                c =  nav +c   
                print("C-PointSet　%6.2f" %c)
                time.sleep(1)
        elif ( key == 7 ): #基準線交換
                base = ~base
                print("基準線を変更しました" )
                time.sleep(1)

        elif ( key == 0 ):
            d = ~d
            print("マーカー反転")
            time.sleep(2)
        elif ( key == 12 ): # [#]
            print("シャットダウン")
            time.sleep(2)
            os.system("sudo shutdown -h now")
        elif ( key == 9 ): 
            print("再起動")
            time.sleep(2)
            os.system("sudo reboot")
        elif ( key == 3):
            view = ~ view
        elif ( key == 6):
            print("5秒停止")
            time.sleep(5)

        else :
            nowpoint = setpoint()
            if (base == 0) :
                ax = _ax
                ay = _ay
                bx = _bx
                by = _by
                blf = "①"
            else :
                ax = aax
                ay = aay
                bx = bbx
                by = bby
                blf = "②"
                
            
            try :
                nx = float(nowpoint[2]) #基準点からのXｍ
                ny = float(nowpoint[3]) #基準点からYｍ
                nq = float(nowpoint[5]) #1:FIX 2:Float 5:single
                nst = int(nowpoint[6]) #衛星数
            except :
                print("Set error")
                
            rad = math.atan2(( by - ay ),( bx - ax )) #atan2 -180<deg<180

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
            #print("Distance",int(dist))
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
            r[4] = r[3]
            r[3] = r[2]
            r[2] = r[1]
            r[1] = r[0]
            r[0] = [qx,qy]
            sx = r[4][0] - r[0][0]
            sy = r[4][1] - r[0][1]
            sz = math.sqrt(math.pow(sx,2) + math.pow(sy,2))
            #print("sx,sy,sz",sx,sy,sz)
#表示
            if (view == 0 ) :
                print(fig)
                print("Nav %+4d cm" % nav)
                print("工程 %d LINE %s" %(koutei,revfig))
                print("Q = %d 衛星数　%d 角度%5.1f° %s" %(nq,nst,math.degrees(rad),blf))
                print("Dist %d 速度　%d cm/s" %(dist,sz*100))

            else :
                print(fig)
            
            
            

except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
GPIO.cleanup()


