#!/usr/bin/python3
'''
トラクタ　ロータリー2ｍ
wide = 195
LED表示　ledarw
圃場SHP読み込み getshp
[0]連番[1]面積[2]ID[3]圃場名[5]A-lat[6]A-lon[7]B-lat[8]B-lon
圃場面積　作業面積　残り時間表示
Auto pre-set baseline
機体傾斜補正MPU60503軸ジャイロ　I2c 

pip3 install pyshp Shapely pymap3d
'''

import socket , time ,math 
from io import StringIO
import RPi.GPIO as GPIO
import shapefile
from shapely.geometry.point import Point 
from shapely.geometry import shape 
from pymap3d.enu import  geodetic2enu
from datetime import datetime
from ledarw import ledarw
from keypad import keypad_get
from MPU6050 import MPU6050



host = '127.0.0.1' #localhost
port = 52001 #enu
bufsize = 150
wide = 195 #作業機幅cm
hori = 5 #水平補正
keisya = 0
ant_h = 220 #アンテナ高さcm
margin = 20 #shpとの余裕分cm
ax = 0 ;ay = 0;bx = 1 ;by = -1
_ax = 0;_ay = 0;_bx = 1;_by = 0;_rad = 0
aax = 0;aay = 0;bbx = 0;bby = 0;rrad = 0
base = False
area = 0
c = 0 #offset cm →｜←
d = True  #マーカー方向　枕2工程 :False  枕3工程 ：True
wra = -1 #levelは操舵方向：−１　　levelはズレ方向：+1
r = [[0,0]]*2
rev = 1
nav = 0
nx = 0;ny = 0;nq = 0;nh= 0
I = '|'#level
O = ' '
view = False
now = datetime.now()
pointfile = '/home/pi/RTKLIB/rtklog/POINTlog_{0:%Y%m%d%H%M}.pos'.format(now)
shpfile = '/home/pi/SHP/2019utf_WGS84_AB.shp'
menseki  = 0;kyori = 0;menseki_total =0
basellh = (34.0000000,136.000000,87.00) #RTK_BASE lat(deg) lon(deg) heigh(m)
GPIO.setmode(GPIO.BOARD)

#ポジションレバー
key_u = 12
GPIO.setup(key_u,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#キーパッド
key_y = (37 ,35 ,33 ,31 )
key_x = (29 ,23 ,21)
#LED
ledpins =  (24,40,38,26,36,32,32,22,18) #0~6:LEDカソード　7,8:アノードコモンLR
GPIO.setup(ledpins,GPIO.OUT)



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

#shp属性を取得
def  getshp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 52002))#llh
    buff = StringIO()
    data = sock.recv(bufsize)    
    sock.close()
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('\n', '')
    dlist = data.split()
    try : 
        point = ( float(dlist[3]) , float(dlist[2]) )#（経度lon、緯度lat）
        shp = shapefile.Reader(shpfile) 
        all_shapes = shp.shapes() 
        all_records = shp.records()
        for i in range(len(all_shapes)):
            boundary = all_shapes[i] 
            if Point(point).within(shape(boundary)): 
               this_record= all_records[i] [:]
               print( "圃場データ",this_record[2:4]    )
               return this_record
        print("NO SHP DATA")
        return 0
    except :
        #print("getshp error")
        return 0

#MPU6050
i2c_bus = 1 #pin3=SDA pin5=SCL
device_address = 0x68
#キャリブレーション数値設定 水平に置き　MPU6050_cal.py　を実行し計算結果を代入
x_accel_offset = -2085
y_accel_offset = -2322
z_accel_offset = 1122
x_gyro_offset = 71
y_gyro_offset = -24
z_gyro_offset = 25

enable_debug_output = False
mpu = MPU6050(i2c_bus, device_address, x_accel_offset, y_accel_offset,
              z_accel_offset, x_gyro_offset, y_gyro_offset, z_gyro_offset,
              enable_debug_output)
mpu.dmp_initialize()
mpu.set_DMP_enabled(True)#DMP (Digital Motion Processor) 
mpu_int_status = mpu.get_int_status()
packet_size = mpu.DMP_get_FIFO_packet_size()
FIFO_buffer = [0]*64
FIFO_count_list = list()
#傾斜cm取得
def roll_MPU(ant_h):
    FIFO_count = mpu.get_FIFO_count()
    mpu_int_status = mpu.get_int_status()
    if (FIFO_count == 1024) or (mpu_int_status & 0x10):
        mpu.reset_FIFO()
        return None
    elif (mpu_int_status & 0x02):
        while FIFO_count < packet_size:
            FIFO_count = mpu.get_FIFO_count()
        FIFO_buffer = mpu.get_FIFO_bytes(packet_size)
        accel = mpu.DMP_get_acceleration_int16(FIFO_buffer)
        quat = mpu.DMP_get_quaternion_int16(FIFO_buffer)
        grav = mpu.DMP_get_gravity(quat)
        roll_pitch_yaw = mpu.DMP_get_roll_pitch_yaw(quat, grav)
        keisya_rad=roll_pitch_yaw.x #MPUの置き方によってx,y,zのうち適切なものを
        #keisya_rad=roll_pitch_yaw.y
        #keisya_rad=roll_pitch_yaw.z
        rollcm = ant_h * math.sin(keisya_rad)
        return rollcm
      

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
                blf = "Auto"
                rad = rrad
            try :
                nx = float(nowpoint[2]) #基準点からのeast(m)
                ny = float(nowpoint[3]) #基準点からnorth(m)
                nh = float(nowpoint[4]) #基準点からのup(m)
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
#傾斜計算
            nrollcm = roll_MPU(ant_h)
            while (nrollcm == None) or (nrollcm > 50)  :
                nrollcm = roll_MPU(ant_h)
            else:
                keisya  = nrollcm - hori
            arw -= keisya # [-=]:左上がりでkeisya>0　[+=]:右上がりでkeisya>0
            nav_roll = arw * rev
#arw反転
            arw　*=　wra              

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
#作業時間予測
            if (spd != 0):
                resttime = (area - menseki) / (0.6 * spd *wide) #残り面積(㎡）/作業速度（㎡/分）
            else:
                resttime = 999
            if (resttime > 999):
                resttime =999
            elif (resttime < -99):
                resttime = -99
#LED
            ledarw( arw , ledpins)       
#表示
            if view == 0  :
                if nq == 1:
                    print("\033[32m%s\033[0m" %fig)
                elif nq == 2 :
                    print("\033[33m%s\033[0m" %fig)
                else :
                    print("\033[31m%s\033[0m" %fig)
#                print("\033[35m    Nav %+4d cm   工程 %d\033[0m" %(nav,koutei))
                print("\033[35m    Nav %+4d cm   工程 %d\033[0m" %(nav_roll,koutei))
                print("  傾斜 =%+3d　LINE %s %s　" %(keisya,revfig,blf)) 
                print("  c=%d　速度%4.1f km/h"  %(c,spd*3.6))
                print("　残り　%3d 分" %resttime)
                print("　圃場=%d㎡作業＝%d㎡" %(area,menseki))              
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
                c +=  nav_roll   
                print("C-PointSet　%6.2f" %c)
                time.sleep(1)
        elif ( key == 9 ): #Ex 基準線交換
                base = not(base)
                print("基準線を変更しました" )
                time.sleep(1)

        elif ( key == 6 ):
            d = not(d)
            print("マーカー反転")
            time.sleep(1)
#        elif ( key == 3 ): # [#]
#            print("シャットダウン")
#            time.sleep(2)
#            os.system("sudo shutdown -h now")
#        elif ( key == 6 ): 
#            print("再起動")
#            time.sleep(2)
#            os.system("sudo reboot")
#        elif ( key == 10):#総面積リセット
#            menseki_total = 0
#            print("総面積リセット")
#            time.sleep(2)      

        elif ( key == 7): #表示切り替え
            view = not(view)
            time.sleep(1)
#        elif ( key == 8):#PointSave
#            fileobj = open(pointfile, "a", encoding = "utf-8")
#            savepoint = "  ".join(setpoint())
#            fileobj.write(savepoint)
#            fileobj.write("\n")
#            fileobj.close()
#            print("PointSave")
#            time.sleep(1)
        elif ( key == 8 ): #水平補正
                hori +=  keisya  
                print("水平補正　%3.1f" %hori)
                time.sleep(1)

        elif ( key == 11):#面積リセット
            menseki = 0
            print("作業面積リセット")
            time.sleep(1)

#        elif ( key == 10):#half
#            c += wide/2
#            print("Half Wide Offset")
#            time.sleep(2)

        elif ( key == 10):#距離リセット
            kyori = 0
            print("走行距離リセット")
            time.sleep(1)
        elif ( key == 12):#shp属性を取る
            shpdata=getshp()
            try:
                if shpdata !=0:
                    area = shpdata[1] #2番目に面積レコード
                    if shpdata[5] != 0:
                        (aax,aay,aah) = geodetic2enu(float(shpdata[5]) ,float(shpdata[6]) ,nh,basellh[0] ,basellh[1] ,basellh[2])
                        (bbx,bby,bbh) = geodetic2enu(float(shpdata[7]) ,float(shpdata[8]) ,nh,basellh[0] ,basellh[1] ,basellh[2])
                        rrad =math.atan2(( bby - aay ),( bbx - aax ))
                        base = True
                        c = -wide /2 -margin #4工程から開始
                        menseki = 0
                        print("Auto Set Line")
                    time.sleep(1) 
                else :
                    area = 0
                time.sleep(1)
                
            except:
                print("Auto set error")
                time.sleep(1)
except socket.error:
    print('socket error')

except KeyboardInterrupt:
    pass
sock.close()
GPIO.cleanup()
