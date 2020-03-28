# ナビプログラム（Python）  
初心者の書いたプログラムですが基準線に平行な線を案内するプログラムです  
簡単に説明すると  
・socketモジュールでRKTLIBからxy座標を受け取ります  
・A点B点の基準線座標からatan2関数で角度radを求める  
・P点のxy座標をA点に平行移動し-rad回転させると基準線からの距離distが求められる  
・基準線からの距離distを作業機幅wideで割ったあまりがズレである  
・あとはターンのたびに左右を反転  
・作業していくうちに出てくるズレをオフセット  
・速度作業面積の計算など  
  
**gpsnavi.py**  
```python:gpsnavi.py
# !/usr/bin/python3
import socket , time ,math 
from io import StringIO
import RPi.GPIO as GPIO
from fabric.colors import red, green ,blue ,magenta,yellow #カラー化 $pip3 install fabric　しておく
# 初期化
host = '127.0.0.1' #localhost
port = 52001
bufsize = 256
wide = 180  #作業機幅cm
a_hokyu = 1000 #A補給面積㎡
b_hokyu = 3000 #B補給面積㎡
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
file = 'pointlog.txt'
menseki  = 0
menseki_total = 0
soukou = 0
# キーパッド
GPIO.setmode(GPIO.BCM)
key_x = [13 ,19 ,26 ]
key_y = [9 ,11 ,5 , 6]
GPIO.setup(key_y,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(key_x,GPIO.OUT)
# 作業機昇降スイッチ
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
# 座標取得
def setpoint():
    
    buff = StringIO()
    data = sock.recv(bufsize)
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('b', '')
    dlist = data.split()
    buff.close()
    if len(dlist) < 15 :
        print("setpoint re-try")
        setpoint()
    return dlist

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
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
        elif ( key == 4 ):#AA
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
                print("%6.0f cmオフセットしました" %c)
                time.sleep(1)
        elif ( key == 6 ): #Ex 基準線交換
                base = ~base
                print("基準線を変更しました" )
                time.sleep(1)

        elif ( key == 9 ):#D
            d = ~d
            print("マーカー反転")
            time.sleep(2)
        elif ( key == 7): #V 表示切り替え
            view = ~ view
        elif ( key == 11):#Atrip面積リセット
            menseki = 0
            print("Ａトリップ面積リセット")
            V = '▲'
            time.sleep(2)
        elif ( key == 0):#Btrip面積リセット
            menseki_total = 0
            print("Ｂトリップ面積リセット")
            V = '▲'
            time.sleep(2)
        elif ( key == 12):#距離リセット
            soukou = 0
            print("走行距離リセット")
            time.sleep(2)
        elif ( key == 8):#PointSave
            fileobj = open(file, "a", encoding = "utf-8")
            savepoint = "  ".join(setpoint())
            fileobj.write(savepoint)
            fileobj.write("\n")
            fileobj.close()
            print("PointSave")
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

            except :
                print("Set error")
                
            rad = math.atan2(( by - ay ),( bx - ax )) #atan2 -180<deg<180

            px = nx - ax
            py = ny - ay
            qx = px*math.cos(-rad)-py*math.sin(-rad) #-rad回転
            qy = px*math.sin(-rad)+py*math.cos(-rad) #y座標が基準線からの距離

            
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
            if rev == 1  :  #LINE(基準線）方向
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
            if ( GPIO.input( 10 ) == 0 ):#作業機が下りたら
                menseki += sz * wide * 0.01 #m2
                if menseki > a_hokyu:
                    V = '△'
                menseki_total += sz * wide * 0.01 #m2
                if menseki_total > b_hokyu:
                    V = '▽'
                soukou += sz #m

 #表示
            if (view == 0 ) :
                print(green(fig))
                print(magenta(fig))
                print(magenta("    Nav %+4d cm   工程 %d" %(nav,koutei)))
                print(" LINE %s   %s" %(revfig,blf)) 
                print(" Q = %d  速度%4.1f km/h"  %(nq,spd*3.6))
                #print(" Q = %d  速度　%d cm/s" %(nq,spd*100))
                print(" Ａ %.0f ㎡ Ｂ %.0f ㎡ " %(menseki,menseki_total))
                print(" 距離 %.2f m" %soukou)                      
            else :
                if nq == 1 :
                    print(green(fig))
                elif nq == 2 :
                    print(yellow(fig))
                else :
                    print(red(fig))
except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
GPIO.cleanup()
```  
  
  
# 入出力装置  
・入力　キーパッド　薄膜パネルスイッチ  
http://www.aitendo.com/product/4736  
出力１　GPIOピンからLEDを点灯  
出力２　スマートフォンにVNCViewerをインストールしてRaspberry Piのデスクトップを表示  
https://www.realvnc.com/en/connect/download/viewer/  
端末アプリのLXterminalに出力（フォントを大きくして見やすくします）  
実行ファイルを作成　実行権限を付ける  
  
**gpsnavi.sh**  
```sh:gpsnavi.sh
# !/bin/sh
/usr/bin/lxterminal -e python /home/pi/gpsnavi.py
```  
  
autostartファイルをつかってGUIで自動起動できるようにしておく  
  
[続く](https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その３）.md)  
