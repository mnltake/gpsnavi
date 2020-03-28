# 目的#  
これまでの話はGPSの位置情報からshpファイルを作ることでしたが、逆にroverの位置情報から登録してあるshpファイルのポリゴンの属性を取り出します。  
以前の記事　[GPSのデータを使ってシェイプファイルの作成](https://github.com/mnltake/gpsnavi/blob/master/GPSのデータを使ってシェイプファイルの作成.md)  
# 参考リンク#  
ほとんどここのコピペです。  
GPSのポイントがシェイプファイルのポリゴンの中にある(within)かどうかを判定します  
Finding out if coordinate is within shapefile (.shp) using pyshp?-StackExchange  
https://gis.stackexchange.com/questions/250172/finding-out-if-coordinate-is-within-shapefile-shp-using-pyshp  
  
https://pypi.org/project/pyshp/  
https://pypi.org/project/Shapely/  
必要なモジュールのインストール  
`~$pip3 install pyshp `  
`~$sudo apt-get install libgeos-dev`  
`~$pip3 install Shapely`  
  
例えば[PMS](http://www.aginfo.jp/PMS/)で使っているシェイプファイルをラズベリーパイにコピー（**＊下記注**）  
.shpだけでなく.dbf .shx .prj など拡張子の違うものも一緒にコピーしておく  
  
  
~~直角平面座標なのでroverの位置は単純にbaseの(x,y)座標に相対距離（enu)を足すだけで求められる（はず）~~  
  
**↑と思っていたら違うみたい。baseから離れるとズレてくる。簡単じゃないようだう～ん…  
数mのズレが許容されるなら以下の方法で**  
  
緯度経度から直角平面座標への変換はこちらを使いました  
QuickConvert  
http://asp.ncm-git.co.jp/QuickConvert/BL2TM.aspx  
  
[Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その２）](https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その２）.md)  
gpsnavi.pyに以下を追加します。  
  
**gpsnavi.py**  
```python:gpsnavi.py
import shapefile
from shapely.geometry.point import Point 
from shapely.geometry import shape 
(略）
# shp属性を取得
def  getshp():
    basepoint = [-xxxxx.xx ,-yyyyyy.yy] #base局の直角平面座標（x,y）
    filepath = '/home/pi/2018utf.shp ' #shpファイルのパス（utf-8エンコード済み）
    pointlist = setpoint()
    point = ( float(pointlist[2]) +basepoint[0] , float(pointlist[3]) +basepoint[1] ) #rover局の座標
    shp = shapefile.Reader(filepath) #shpファイルの読み込み
    all_shapes = shp.shapes() # 全ポリゴン取得
    all_records = shp.records()#ポリゴンの属性を取得

    for i in range(len(all_shapes)):
        boundary = all_shapes[i] # ポリゴン境界
        if Point(point).within(shape(boundary)): # pointがポリゴンの中にあるか判定
           this_record= all_records[i][:9] #該当するポリゴンの属性を取得
           print( "圃場データ",this_record )
           return this_record
    print("圃場データはありません")
    return
(略）
        key = keypad_get()
(略）
        elif ( key == 12):#shp属性を取る
            getshp()
            time.sleep(5)
```  
  
# 応用できること#  
  
- 機械を圃場に入れボタン一つで地番、面積、所有者名、品種など属性テーブルに記録されている情報を取り出せる  
- 基準線A点B点をポリゴンの属性内に登録しておけば毎回設定しなくても自動的に読み出してセットできる。  
- 圃場に出入りした時間がわかるので手入力しなくても作業時間を記録できる  
- 圃場面積・作業面積・速度からその圃場の作業終了時間が予測できる  
  
# 課題#  
PMSでは圃場シェイプファイルの属性(フィールド）名に日本語(Shift_jis ?)を使っているのでそのままでは読み込めない。QGISやExcelで英数に直しutf-8 でエンコードし直して読み込めた。もっとスマートな方法があるはず。ファイルの同期とかできたら便利そうだが。  
  
## 追記（2018/12/7）##  
shpファイルを参照座標系：WGS84に変換して  
point = (経度lon　, 緯度lat)  
とすれば解決しそう。  
なおrtkrcvのオプションとして　-m 52002 をつけることで　localhost:52002にllh(緯度経度）を含むデータが流れてくる。outstr1,outstr2,-mの計3種類の形式で出力される。  
  
**getshp**  
```python:getshp

# shp属性を取得
def  getshp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 52002))
    buff = StringIO()
    data = sock.recv(bufsize)
    sock.close()
    buff.write(data.decode('utf-8'))
    data = buff.getvalue().replace('\n', '')
    dlist = data.split()
    try : 
        point = ( float(dlist[3]) , float(dlist[2]) )#（経度lon、緯度lat）
        shp = shapefile.Reader('/home/pi/SHP/2019utf_WGS84.shp') #WGS84測地系
        all_shapes = shp.shapes() 
        all_records = shp.records()
        for i in range(len(all_shapes)):
            boundary = all_shapes[i] 
            if Point(point).within(shape(boundary)): 
               this_record= all_records[i] [:]
               print( "圃場データ",this_record[9:11]    )
               return this_record
        print("NO SHP DATA")
        return 0
    except :
        getshp()

```  
