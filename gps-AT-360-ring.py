#!/usr/bin/python3
# coding=utf-8

import socket , time ,math #,os
from io import StringIO
import RPi.GPIO as GPIO
from neopixel import *
from color_arw1 import colorarw

#host = '127.0.0.1' #localhost
port = 52001
host = '192.168.3.14' #tab
#port = 52004
bufsize = 200
buff = StringIO()
wide = 350  #作業機幅cm
a_hokyu = 5000 #A補給面積㎡
b_hokyu = 10000 #B補給面積㎡
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
base = 0
r = [[0,0]]*2
rev = 1
nav = 0
nx = 0
ny = 0
nq = 0
nt = 0.2
V = '▲'
I = '|'
O = ' '
view = 0
file = 'ATpointlog.txt'
menseki  = 0
menseki_total = 0
soukou = 0

LED_COUNT      = 12     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#キーパッド
GPIO.setmode(GPIO.BCM)
key_x = [13 ,19 ,26 ]
key_y = [9 ,11 ,5 , 6]
GPIO.setup(key_y,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(key_x,GPIO.OUT)
#ポジションレバー
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_UP) 

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
    #print(data)
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('\n', '')
    dlist = data.split()
    #print(dlist)
    #print(len(dlist))
    buff.close()
    if len(dlist) < 15 :
        print("setpoint re-try")
        setpoint()
    return dlist

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    while True:
        key = keypad_get()
        if ( key == 1 ): #A
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
                
        elif ( key == 2 ): #B
            setBlist = setpoint()
            try :
                _bx = float(setBlist[2])
                _by = float(setBlist[3])
                print("B-PointSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)
        if ( key == 4 ):#AA
            setAAlist = setpoint()
            try :
                aax = float(setAAlist[2])
                aay = float(setAAlist[3])
                print("AA-PointSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)
                
        elif ( key == 5 ):#BB
            setBBlist = setpoint()
            try :
                bbx = float(setBBlist[2])
                bby = float(setBBlist[3])
                print("BB-PintSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)                
        elif ( key == 3 ): #C 0補正
                c =  nav +c   
                print("C-PointSet　%6.2f" %c)
                time.sleep(1)
        elif ( key == 6 ): #Ex 基準線交換
                base = ~base
                print("基準線を変更しました" )
                time.sleep(1)

        elif ( key == 9 ):#D
            d = ~d
            print("マーカー反転")
            time.sleep(1)

        elif ( key == 7): #V 表示切り替え
            view = ~ view

        elif ( key == 11):#wide 350
            wide = 350
            print("wide=350")
            time.sleep(1)
        elif ( key == 0):#wide 700
            wide = 700
            print("wide=700")
            V = '△'
            time.sleep(1)
        elif ( key == 8):#half
            c += wide/2
            print("C += Wide/2")
            time.sleep(1) 
        
        else :
            nowpoint = setpoint()
            if (base == 0) :
                ax = _ax
                ay = _ay
                bx = _bx
                by = _by
                blf = "A-B"
            else :
                ax = aax
                ay = aay
                bx = bbx
                by = bby
                blf = "AA-BB"
                
            
            try :
                nx = float(nowpoint[2]) #基準点からのXｍ
                ny = float(nowpoint[3]) #基準点からYｍ
                nq = float(nowpoint[5]) #1:FIX 2:Float 5:single
                nst = int(nowpoint[6]) #衛星数
                #nt = float(nowpoint[1]) #時間秒
                #if float(nowpoint[7]) < 0.02 :
                #    seido ='◎'
                #else :
                #   seido =''
            except :
                print("Set error")
                #          print(nowpoint)
                
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
                fig = O * w + V + I * w
            elif 2 <= arw  < 20:
                fig = O * w + V + I*level + O *(w -level)
            elif -2 < arw < 2 :
                fig = O * w + V
            elif -20 < arw <= -2:
                fig =O * (w -level) + I * level  + V
            elif arw <= -20:
                fig = I * w + V
                
#colorWipe
            colorarw(strip,arw)               


 
#速度計算
            #for m in range(4, 1) :
            #    r[m] = r[m-1]
            r[1] = r[0]
            r[0] = [qx,qy]
            sx = r[0][0] - r[1][0]
            sy = r[0][1] - r[1][1]
            #st = r[0][2] - r[1][2]
            #st = 0.2
            #if st == 0 :
            #    st = 0.2
            sz = math.sqrt(math.pow(sx,2) + math.pow(sy,2))
            if sz > 4:#72km/h以上はノーカウント
                sz = 0
            spd = sz * 5  #m/s
  
            #print("sx,sy,sz",s[0],s[1],s[2])
#作業面積計算
            if ( GPIO.input( 10 ) == 0 ):
                menseki += sz * wide * 0.01 #m2
                if menseki > a_hokyu:
                    V = '▲'
                menseki_total += sz * wide * 0.01 #m2
                if menseki_total > b_hokyu:
                    V = '▲'
                soukou += sz #m




#表示
            if (view == 0 ) :
                print("\033[32m%s\033[0m" %fig)
                print("\033[32m%s\033[0m" %fig)
                print("\033[35m    Nav %+4d cm   工程 %d\033[0m" %(nav,koutei))
                print(" LINE %s   %s" %(revfig,blf)) 
                print(" Q = %d  速度%4.1f km/h"  %(nq,spd*3.6))
                print(" 幅 =%d" %wide)
                print(" c= %d" %c)                      
            else :
                if nq == 1 :
                    print("\033[32m%s\033[0m" %fig)
                elif nq == 2 :
                    print("\033[33m%s\033[0m" %fig)
                else :
                    print("\033[31m%s\033[0m" %fig)
            
            
except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
GPIO.cleanup()


