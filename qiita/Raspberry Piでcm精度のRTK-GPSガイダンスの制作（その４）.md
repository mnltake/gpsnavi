# Ambientで地図上に表示  
今回はGPS(GNSS)トラッカー（ロガー）機能を追加したいと思います。  
RTKLIBにもWindows用に地図上にプロットするアプリや、後処理でgoogleMapに利用できるkmlファイルに変換機能がありますが、リアルタイムでAndroidスマホ等で地図にプロットするには別にアプリを用意する必要がありました。  
簡単にかつ無料で地図上に位置情報を表示するためにAmbientを利用しました。  
  
# 参考URL  
ESP8266 ArduinoとGPSモジュールでGPSロガーを作る  
https://qiita.com/AmbientData/items/7f728917ce0df78e7124  
Ambient　IoTデーターの可視化サービス  
https://ambidata.io/  
データーに位置情報を付加する  
https://ambidata.io/docs/geo/  
AmbientのPython/MicroPythonモジュール  
https://github.com/AmbientDataInc/ambient-python-lib  
  
# Pythonプログラム  
Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）  
https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）.md  
にあるrtkrcvの設定ファイルを一部書き換えます  
  
```my.conf
outstr2-type       =tcpsvr
outstr2-path       =:52002
outstr2-format     =llh
```  
**（追記）**  
またはrtkrcvのモニターオプションを利用して  
  
```rtkrcv.sh 
# !/bin/sh
cd /home/pi/RTKLIB/app/rtkrcv/gcc/
./rtkrcv  -o /home/pi/RTKLIB/app/rtkrcv/my.conf -s -d /dev/tty0 -m 52002
```  
Python3モジュールのインストール  
  
```
$ sudo pip3 install git+https://github.com/AmbientDataInc/ambient-python-lib.git
```  
  
**gps-tracker.py**  
```python:gps-tracker.py
# !/usr/bin/python3
import socket
from io import StringIO
import ambient
am = ambient.Ambient(チャネルID,'ライトキー')
host = '127.0.0.1' #localhost
port = 52002
bufsize = 150
timespan = 50 #10s *5Hz =50
def setpoint():
    buff = StringIO()
    data = sock.recv(bufsize)
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('b ', ' ')
    dlist = data.split()
    buff.close()
    return  dlist

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    while True:
        i =0
        for i in range(timespan) :
            dlist = setpoint()
        senddata = {'created': 'YYY-MM-DD HH:mm:ss.sss','d1': float(dlist[4]) ,'lat': float(dlist[2]) ,'lng':float(dlist[3])}
        r = am.send(senddata)
        if r.status_code ==200:
            print('send OK')
        else :
            print('ambientsend error')
except socket.error:
    print('socket error')
except KeyboardInterrupt:
    pass
sock.close()
```  
  
  
# Ambientで表示  
[チャート設定]-[グラフ種類]-[地図]を選択  
![ambient2.jpg](/image/b41029ba-4b1f-a6d8-02ea-c4394eca7ea4.jpeg)  
  
  
d1として高さをデータとして送りました。  
# 応用できること  
・複数者作業中にネット経由で現在位置と進捗状況がスマホの地図上で確認できる  
・例えばECセンサーと組み合わせて土壌肥沃度マップ、収量センサーと合わせて収量マップ、レーザー測量機と組み合わせて精密高低差マップなどが作れる。  
  
  
  
