#!/usr/bin/python3
'''
2021
config.ini
圃場SHP読み込み getshp
[0]連番[1]面積[2]ID[3]圃場名[5]A-lat[6]A-lon[7]B-lat[8]B-lon
圃場面積　作業面積　残り時間表示
Auto pre-set baseline
neopixelLED wcolorarw
1工程飛ばし
UBX Serial('/dev/ttyAMA0')入力
pymap3d log
line bot
rainfall
socket client

pip3 install pyshp Shapely pymap3d rpi_ws281x
'''
import configparser
import time ,os ,math ,serial
import urllib.request
import RPi.GPIO as GPIO
import shapefile
from shapely.geometry.point import Point
from shapely.geometry import shape
from pymap3d.enu import  geodetic2enu
from datetime import datetime
from keypad import keypad_get
from rpi_ws281x import PixelStrip, Color
from neopixel_arw import colorarw,wcolorarw
from readUBX import readUBX
from line_notify_bot import LINENotifyBot
from rainfall import rainfall
import socket,struct

config_ini = configparser.ConfigParser()
config_ini.read('./config.ini', encoding='utf-8')
read_default = config_ini['DEFAULT']
roverName = str(read_default.get('roverName'))
WIDE =int(read_default.get('WIDE'))
wide = WIDE
margin = int(read_default.get('margin'))
ubxPort = str(read_default.get('ubxPort'))
ubxRate = int(read_default.get('ubxRate'))
ax = 0 ;ay = 0;bx = 1 ;by = 0 ;ABsin =0; ABcos = 1
_ax = 0;_ay = 0;_bx = 1;_by = 0;_rad = 0;_ABsin =0;_ABcos =1
aax = 0;aay = 0;bbx = 0;bby = 0;rrad = 0;AABBsin =0; AABBcos =1
base = False
area = 0
c = 0 #offset cm →｜←
Direction = bool(read_default.get('Direction'))
#Direction = True  #マーカー方向　枕2工程 :False  枕3工程 ：True
d = Direction
wra = -1 #levelは操舵方向：−１　　levelはズレ方向：+1
wra *= 2/2 #level１本　2/2:2cm　2/3:3cm 2/4:4cm
r = [[0,0]]*2
rev = 1
nav = 0
nx = 0;ny = 0;nq = 0;nh= 0
I = '|'#level
O = ' '
view = False
shpfile = read_default.get('shpfile')
menseki  = 0;kyori = 0;menseki_total =0
basellh = (float(read_default.get('baselat')),float(read_default.get('baselon')),float(read_default.get('baseh')))
logdir = read_default.get('logdir')

#socket cli
HOST = 'localhost'    # The remote host
PORT = 50001  # The same port as used by the server
bint=b''
old=b''
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


#LINE bot token
line_access_token=read_default.get('line_access_token')
bot = LINENotifyBot(access_token=line_access_token)
# yahoo APIを使うためのKEY
crient_id = read_default.get('yahoo_crient_id')

GPIO.setmode(GPIO.BOARD)

#ポジションレバー
key_u = 19
GPIO.setup(key_u,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#キーパッド
if (roverName=="reTerminal"):
    key_y = (40 ,38 ,36 ,32 )
    key_x = (15 ,18 ,16)
else :
    key_y = (37 ,35 ,33 ,31 )
    key_x = (29 ,23 ,21)

# neopixcel LED strip
LED_COUNT      = 26     # Number of LED pixels.13
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!)=Pin12(BOARD)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

#座標取得
def setpoint():
    try:
        buffsize = 172
        with serial.Serial(ubxPort, ubxRate, timeout=1) as ser:
            readbytes =[]
            for i in range(buffsize):
                readbytes.append(ser.read())
        r=readUBX(readbytes)
    except:
        return None
    return r

#shp属性を取得
def  getshp():
    try :
        nowmsg = setpoint()
        point =( nowmsg['Lon']*0.0000001, nowmsg['Lat']*0.0000001)#（経度lon、緯度lat）
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

#wait NTPtimeSet
def wait_NTP():
    try:
        ntpnow=datetime.now()
        nowmsg =setpoint()
        ntpMS="{0:%M%S}".format(ntpnow)
        gpsMS="{:02d}{:02d}".format(nowmsg['min'],nowmsg['sec'])
        if (ntpMS != gpsMS):
            return True
        else:
            return False
    except:
        return True

#make file
def make_file():
    now =datetime.now()
    folder  = logdir + roverName +'log_{0:%Y%m}/'.format(now)
    file = '{0:%m%d-%H%M}.csv'.format(now)
    print(file)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder,file

#ファイル保存
def write_file(nowmsg,arw):
    savepoint =str(datetime.now())+","+str(nowmsg['Lon']*0.0000001)+","+str(nowmsg['Lat']*0.0000001)+","+str(nowmsg['Height']*0.001)+","+str(nowmsg['carrSoln'])+","+str(nowmsg['gSpeed']*0.001)+","+str(errorarw)+"\n"
    #print(savepoint)
    with open(folder + file, "a", encoding = "utf-8") as fileobj:
        fileobj.write(savepoint)



#time.sleep(10)
try:
    while wait_NTP():
        print("waiting NTP ")
        time.sleep(1)
    print("NTP synchro")
    (folder,file)=make_file()
    header ="JST,longitude,latitude,Height,gps_qual,gSpeed,errorarw\n"
    with open(folder + file, "a", encoding = "utf-8") as fileobj:
        fileobj.write(header)
    while True:
        try:
            s.connect((HOST, PORT))
        except:
            pass
        else:
            break
    os.system('wmctrl -a "TFT Simulator"' )
    while True:
        key = keypad_get(*key_x, *key_y)
        # touch_key = s.recv(1)
        # print(touch_key)
    #main
        if (key == 0 ):
            
            nowmsg = setpoint()
            while nowmsg ==None:
                print('seterror')
                nowmsg = setpoint()
            #write_file(nowmsg)
            # print(nowmsg)
            if (base == 0) :
                ax = _ax
                ay = _ay
                bx = _bx
                by = _by
                blf = "A-B "
                rad = _rad
                ABsin = _ABsin
                ABcos = _ABcos
            else :
                ax = aax
                ay = aay
                bx = bbx
                by = bby
                blf = "Auto"
                rad = rrad
                ABsin = AABBsin
                ABcos = AABBcos
            try :
                nx = float(nowmsg['E']) #基準点からのeast(cm)
                ny = float(nowmsg['N']) #基準点からnorth(cm)
                #nh = float(nowmsg['D']) *-10 #基準点からのup(cm)
                nq = float(nowmsg['carrSoln']) #2:FIX 1:Float 0:single

            except :
                pass

            px = nx - ax
            py = ny - ay
            qx = px*ABcos - py*ABsin #-rad回転
            qy = px*ABsin + py*ABcos


            if qy < 0 : #右回り
                dist = -qy -c #cm
                turn = -1
            else : #左回り
                dist = qy -c #cm
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


            if arw <-15:
                errorarw = ""
            elif arw > 15:
                errorarw = ""
            else :
                errorarw = arw
#arw反転
            arw *= wra

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
            spd = nowmsg["gSpeed"] /1000 #m/s
            sz = spd /5
#作業面積計算
            if ( GPIO.input( key_u ) == 0 ):
                menseki += sz * WIDE * 0.01 #m2
                kyori += sz #m
                menseki_total += sz * WIDE * 0.01 #m2
#作業時間予測
            if (spd != 0):
                resttime = (area - menseki) / (0.6 * spd *WIDE) #残り面積(㎡）/作業速度（㎡/分）
            else:
                resttime = 999
            if (resttime > 999):
                resttime =999
            elif (resttime < -99):
                resttime = -99

#neopixcel LED
#            wcolorarw (strip , arw)
#表示

            if view == True  :
                if nq == 2:
                    print("\033[32m%s\033[0m" %fig) #green
                elif nq == 1 :
                    print("\033[33m%s\033[0m" %fig)#brown
                else :
                    print(fig) #black
                print("\033[35m    Nav %+4d cm   工程 %d\033[0m" %(nav,koutei))
                print("  幅=%3d   LINE %s %s　" %(wide,revfig,blf))
                print("  c=%3d　%4.2f km/h "  %(c,spd*3.6))
                print("　残り　%3d 分" %resttime)
                #print("　GPSTIME　%d ms" %nowmsg['iTow'])
                if ( GPIO.input( key_u ) == 0 ):
                    print("　圃場=%4d㎡\033[35m作業＝%4d㎡\033[0m" %(area,menseki))
                else :
                    print("　圃場=%4d㎡作業＝%4d㎡" %(area,menseki))
                print("")
                    #print("lon:%3.6f  lat:%2.7f" %(nowmsg['Lon']*0.0000001,nowmsg['Lat']*0.0000001))

            # else :
            #     if nq == 2 :
            #         print("\033[32m%s\033[0m" %fig)
            #     elif nq == 1:
            #         print("\033[33m%s\033[0m" %fig)
            #     else :
            #         print("\033[31m%s\033[0m" %fig)
# # ファイル保存
            # try:
            #     write_file(nowmsg,errorarw)
            # except:
            #     pass
# socket send
        try:
            buff=b''
            buff=struct.pack("hhHHhhIIbb",int(arw),int(nav),int(koutei),int(wide),int(rev),int(c),int(area),int(menseki),int(base),int(key))
            s.sendall(buff)
            # print(buff)

        except:
            pass
#key入力時

        if ( key == 1 ):
            Amsg = setpoint()
            while Amsg == None:
                Amsg = setpoint()
            try :
                _ax = float(Amsg['E'])
                _ay = float(Amsg['N'])
                c = 0
                _rad =math.atan2(( _by - _ay ),( _bx - _ax ))
                _ABsin = math.sin(-_rad)
                _ABcos = math.cos(-rad)
                print("A-PointSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)

        elif ( key == 2 ):
            Bmsg = setpoint()
            while Bmsg == None:
                Bmsg = setpoint()

            try :
                _bx = float(Bmsg['E'])
                _by = float(Bmsg['N'])
                _rad =math.atan2(( _by - _ay ),( _bx - _ax ))
                _ABsin = math.sin(-_rad)
                _ABcos = math.cos(-_rad)
                print("B-PointSet")
                time.sleep(1)
            except :
                print("Set error")
                time.sleep(1)

        elif ( key == 4 ):#隣接
            wide = WIDE
            print("wide = %d" %wide)
            time.sleep(1)
        elif (key == 5 ):#1本飛ばし
            wide = WIDE * 2
            print("wide = %d" %wide)
            time.sleep(1)

        elif ( key == 3 ): #0補正
                c +=  nav
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
            if view:
                os.system('wmctrl -a "TFT Simulator"' )
            else :
                os.system('wmctrl -a "sudo"' )
            time.sleep(1)
    
        elif ( key == 8 ):#rainfall
            os.system('wmctrl -a "sudo"' )
            for i in range(6):
                print(" ")
            try:
                rainfall(nowmsg['Lon']*0.0000001, nowmsg['Lat']*0.0000001 , crient_id)
            except :
                print("No Yahoo crient_id")
            os.system('wmctrl -a "TFT Simulator"' )
            # time.sleep(1)

        elif ( key == 11):#面積リセット
            menseki = 0
            print("作業面積リセット")
            time.sleep(1)

        elif ( key == 10):#half
            c += wide/2
            print("Half Wide Offset")
            time.sleep(1)


        elif ( key == 12):#shp属性を取る
            shpdata=getshp()
            os.system('wmctrl -a "sudo"' )
            try:
                if shpdata !=0:
                    area = shpdata[1] #2番目に面積レコード
                    if shpdata[5] != 0:
                        wide = WIDE
                        (aax,aay,aah) = (geodetic2enu(float(shpdata[5]) ,float(shpdata[6]) ,nowmsg["Height"]*0.001,basellh[0] ,basellh[1] ,basellh[2])) 
                        (bbx,bby,bbh) = (geodetic2enu(float(shpdata[7]) ,float(shpdata[8]) ,nowmsg["Height"]*0.001,basellh[0] ,basellh[1] ,basellh[2]))
                        aax *= 100 #cm
                        aay *= 100
                        bbx *= 100
                        bby *= 100
                        rrad =math.atan2(( bby - aay ),( bbx - aax ))
                        AABBsin = math.sin(-rrad)
                        AABBcos = math.cos(-rrad)
                        base = True
                        c = -wide /2 -margin #枕+1工程から開始
                        menseki = 0
                        d = Direction
                        line_bot_message =roverName +'が[' + shpdata[3] +']の作業を始めました'
                        print("Auto Set Line")
                        bot.send(message=line_bot_message,)
                    time.sleep(1)
                else :
                    area = 0
                time.sleep(1)
                os.system('wmctrl -a "TFT Simulator"' )
            except:
                print("Auto set error")
                time.sleep(1)
                os.system('wmctrl -a "TFT Simulator"' )

except KeyboardInterrupt:
    os.system('wmctrl -c "TFT Simulator"' )
GPIO.cleanup()
