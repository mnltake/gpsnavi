初投稿からちょうど1年経ちました。思った以上の閲覧や いいね ありがとうございました。  
  
これまではRTKLIBを使って座標を得ていたんですが、低価格高性能2周波受信機[u-blox ZED-F9P](https://www.u-blox.com/ja/product/zed-f9p-module)が発売されぜひ試して見たいと思っていた所、どうやら内蔵のRTKエンジンを使ったほうが性能を発揮できるらしいとの話。  
 一般的にGPS受信機はNMEAフォーマットの緯度経度等の情報を出力するので平面座標で何cm動いたかはそこから計算する必要があります。その点RTKLIBはENU座標出力が付いていたので扱いやすかったです。  
しかしpythonには便利なモジュールが公開されているので,それらを使えばできたので紹介したいと思います  
  
前回まで  
Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１～４）  
https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）.md  
https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その２）.md  
https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その３）.md  
https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作（その４）.md  
ハードの材料は受信機以外は同じです  
  
# 参考リンク  
F9PでRTK  
https://qiita.com/yasunori_oi/items/47587098f2c177fe8e47  
simpleRTK2B  
https://qiita.com/yasunori_oi/items/b635ae2fb81fb770be93  
F9Pで基地局  
https://qiita.com/yasunori_oi/items/a6cf9323fc2c94acd22a  
ZED-F9Pの設定方法  
http://www.denshi.e.kaiyodai.ac.jp/gnss_tutor/pdf/st_190310_2.pdf  
  
# 基準局（Base)  
基準局からRTCM 出力の方法はトラ技のマニュアルにも詳しくあるので割愛  
上記リンクを参照  
受信機には  
**NEO-M8P-2** [トラ技RTKスタータキット基準局用【TGRTK-A】](https://shop.cqpub.co.jp/hanbai/books/I/I000238.htm)　か  
**ZED-F9P** [simpleRTK2B](https://www.ardusimple.com/product/simplertk2b-basic-starter-kit-ip65/)など　が必要です  
  
# 移動局（Rover)  
- u-centerの設定  
  
UBX-CFG-DGNSS-[3-RTK fixed]  
UBX-CFG-GNSS-[GPS,BeiDou]  
 **F9Pだとお好みでGalieo,GLONASS,QZSSと選び放題ですが衛星が多ければいいというわけでもないようなので適宜調整して**  
UBX-CFG-PRT-[2-UART2]-in[RTCM]　**ラズパイとはdev/ttyUSB0で繋がってるものとします**  
UBX-CFG-PRT-[3-USB]-out[NMEA]　　**ラズパイとはdev/ttyACM0で繋がってるものとします**  
UBX-CFG-MSG-［F0-00　NMEA　GxGGA］**のみ**出力  
UBX-CFG-TMODE3-[0-Disabled]  
UBX-CFG-NMEA-［High precision modeにチェック]  
UBX-CFG-NAV5-[Dynamic Mode 4-Automotiv],[Fix Mode-3-Auto 2D/3D],[Min SV Elevation-25deg]  
  
[simpleRTK2B](https://www.ardusimple.com/product/simplertk2b-basic-starter-kit-ip65/)ですとUART2はジャンパー1本とmicroUSBケーブルで繋ぐことができます  
https://www.ardusimple.com/simplertk2b-hack-1-unleash-the-usb-power-of-simplertk2b/  
  
- Ntrip Client  
  
受信機にインターネット経由でRTCM信号を入力します  
  
```str2str-in.sh
# ! /bin/sh
cd /home/pi/RTKLIB/app/str2str/gcc/
./str2str  -in ntrip://rtk2go.com:2101/[MountID] -out serial://ttyUSB0:115200
```  
# ナビプログラム（Python）  
  
必要なモジュールをインポートします  
  
```
pip3 install pymap3d　pyserial pynmea2
```  
  
pynmea2  
https://github.com/Knio/pynmea2  
  
  
```gpsnavi-serialNMEA.py
(一部抜粋 ）
import serial
from pymap3d.enu import  geodetic2enu
import pynmea2
basellh = (35.6580992 ,139.74135747 , 63.232) #base deg,deg,m　必ずしも基準局のアンテナの座標でなくても良い任意の所で

# 座標取得
def setpoint():
    with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
        try:
            msg = pynmea2.parse(ser.readline().decode('ascii', errors='replace'))
            if isinstance(msg, pynmea2.types.talker.GGA):
                roverllh =[msg.latitude ,msg.longitude ,msg.altitude] #deg,deg,m
                enu = geodetic2enu(roverllh[0] ,roverllh[1] ,roverllh[2] ,basellh[0] ,basellh[1] ,basellh[2] )
            else:
                setpoint()
        except:
            print('nmea msg parse error')
            return None,None
        return enu ,msg

(enu ,msg) =setpoint()

```  
[Github](https://github.com/mnltake/gpsnavi) で公開  
  
これで以下のような値を取り出せます  
**enu[0]** :baseから東に（m）  
**enu[1]** :baseから北に（m）  
**enu[2]** :baseから上に（m）  
**msg.timestamp** :UTC時  
**msg.latitude** :緯度（deg)  
**msg.longitude** :経度（deg)  
**msg.altitude** :楕円体高（m）  
**msg.geo_sep** :ジオイド高 (m) 標高=楕円体高-ジオイド高  
**msg.gps_qual** :1-Single 5-Float 4-Fix  
  
~~まだF9Pは一台しかないので実際これで2周波の威力を試してはいませんが来シーズンに期待したいです！~~  
評判通り即FIXするだけでなく、アンテナの設置場所も自由度が増しました。  
さらにラズパイの負荷も減らせる方法も次回で記事にしました  
https://github.com/mnltake/gpsnavi/blob/master/u-blox F9P から相対立体座標を受け取る.md  
  
