# 目的  
10年ほど前から農業経営にPMSというGISソフトを利用しており  
これまで1/2500の紙の都市計画図やGoogleMapをスキャンして圃場シェイプファイル(ポリゴン）を作成していました。  
今年からRTK-GPSでcm精度の位置データが取れたのでこれを元に(来るべき自動運転時代に向けて？）精密なシェープファイルを作り直したいと思います。  
  
# 使用するソフト  
**1. RKTLIB**  
GNSS測位用オープンソースプログラムパッケージ  
http://www.rtklib.com/  
  
**2. QGIS**  
オープンソースの地理情報システム  
https://www.qgis.org/ja/site/  
**3. PMS**  
「作業計画・管理支援システム」  
http://www.aginfo.jp/PMS/  
  
  
 **すべて無料で使えます！! 感謝！！**  
  
  
# RTKLIBのposファイルをkmlファイルに変換  
[Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）]  
(https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）.md)  
この通り設定すると/home/pi/RTKLIB/rtklog/ディレクトリに ???_sol.posと緯度経度等のテキストファイルが出力されます。  
GUIの**RTKPOST.exe**を使ってもkmlファイルに変換できますが、ラズパイ上で**pos2kml**で一括に変換したほうが簡単なので  
`cd /home/pi/RTKLIB/app/pos2kml/gcc`  
`./pos2kml /home/pi/RTKLIB/rtklog/*.pos`  
出来たkmlファイルをQGISを使えるPCに転送しておきます  
  
# QGISでkmlファイルを開きトレースしてshpファイルを作る  
QGISの左上の	[ブラウザ]からkmlファイルを選択して開く。座標参照系はWGS84  
![qgis1.jpg](/image/0681d709-fe92-10b7-aedc-374ca3ddf27f.jpeg)  
  
[新規シェープファイルレイヤ]ボタンを押してレイヤー追加。  
エンコード = system  , ジオメトリタイプ = ポリゴン  , 座標参照系は直角平面座標（私のところはⅦ系）  
![qgis3.jpg](/image/d26bd4e3-919f-e3a8-3b68-3d646cfc408f.jpeg)  
  
シェイプレイヤを選択して［編集モード切り替え］-［ポリゴン地物を追加］頂点を右クリックしてポリゴン作成、左クリックで確定。idに連番をつけておきます  
![qgis5.jpg](/image/8be72484-082f-5034-6615-77b26b7b1c01.jpeg)  
  
[フィールド計算機を開く」**area(  \$geometry )**で面積、 **perimeter(  \$geometry )**で周囲長（畦の長さ）  
**x(  \$geometry )**でポリゴン重心のX座標、**ｙ(  \$geometry )**でY座標が求められます  
  
ベクターレイヤを保存  
  
ちなみにQGIS上で国土地理院の様々な地図画像（地理院タイル）を重ね合わせることができ  
例えば基盤整備前の1970年代の航空写真と現在の圃場を比べたりすると意外な発見があって面白いです。  
[QGIS3でウェブ地図利用が劇的に変化した](https://qiita.com/ishiijunpei/items/59136a778a183484734e)  
https://maps.gsi.go.jp/development/ichiran.html  
  
- トラクターの軌跡  
![qgis7.jpg](/image/12b5eef9-d0c0-e3cd-13f5-f2d051d91a8d.jpeg)  
  
- 田植え機の軌跡  
![qgis8.jpg](/image/060f85f7-76d1-10ae-eb5e-fb8b64178449.jpeg)  
  
- コンバインの軌跡  
![qgis9.jpg](/image/702802bc-f04a-a113-faba-5300d99872bc.jpeg)  
  
- 全部重ねるとこんな感じ  
![qgis10.jpg](/image/e9e131ae-a2d8-19fe-642d-c7a390283839.jpeg)  
  
  
# shpファイルをPMSで使う  
これ以降はPMSを利用する場合の説明です  
shpファイルを「圃場図作成（ShapeMaker）」で開く  
属性テーブルを開き編集　LAT/LONフィールドの空セルを右クリック。［緯度経度算出」で自動計算  
面積や連番を「属性間コピー」でコピー  
![qgis13.jpg](/image/f3602a6e-ac69-999f-da33-d60eceabd174.jpeg)  
  
PMS用圃場図シェイプファイルの仕様はマニュアルのP.61にあります  
http://www.aginfo.jp/PMS/Download/PMSMap.pdf  
以上でGPSから圃場図シェイプファイルの出来上がりです。  
  
**追記**  
もし初めてPMSを使う方がいたらRTK-GPSがなくてもQGISで国土地理院の全国最新写真（シームレス）を利用してshpファイルを作成し,上の方法で属性を編集する方法をおすすめします。  
  
PMS付属のShapeMakerはバグがありよく落ちますし、GoogleMapの写真より地理院の方がズームレベルが高いです。  
