RTKLIBの変換機能（pos2kml)を使わなくても直接QGISでposファイルを開ける方法を教わったので使ってみました。  
[前回:GPSのデータを使ってシェイプファイルの作成](https://github.com/mnltake/gpsnavi/blob/master/GPSのデータを使ってシェイプファイルの作成.md)  
  
---  
「新規作成」-「プロジェクトの参照座標系」-「WGS84：投影なし（ESPG:4236）」  
「XYZ　Tiles」-国土地理院タイル　全国最新写真（シームレス）https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg  
をレイヤに追加（以下の　[画像の出典](https://maps.gsi.go.jp/development/ichiran.html) )  
  
「レイヤの追加」-「デリミテッドテキストレイヤの追加」  
![qgis1-1.jpg](/image/100e0d77-6ffd-d799-f9ea-b9ed784084ef.jpeg)  
  
posファイルを選択し　カスタム区切り文字   　-[x]  　空白、- [x] 最初のレコードはフィールド名を保持している、- [x] 空フィールドを削除する  
Xフィールド-「longtitude(deg)」　Yフィールド-「latitude(deg)」  --「追加」  
![qgis1-2.jpg](/image/e8c301f6-2d7c-f6b9-3620-1bd397461946.jpeg)  
  
「レイヤプロパティ」-「シンポロジー」-「Graduated」-「カラム」：height(m）-「モード」：分位数（等級）　シンボル、カラー、分類数はお好みに  
![qgis1-3.jpg](/image/6eccd04d-cba6-3865-17e8-4d44a745c8e1.jpeg)  
  
  
なんとなく高低差が出てる？これは田植機の軌跡なので地表面ではなく耕盤（車輪が沈んだ状態での高さ）ですがそれっぽく見えます。  
![qgis1-4.jpg](/image/f3c57262-dc6a-7e6a-e094-ed5d6c67ed23.jpeg)  
  
別の日のデータではこんな感じでした。左上の圃場は数年前に4枚の田んぼを1枚にまとめたものですがまだムラがあるのがわかります。  
![qgis1-5.jpg](/image/38bf9599-ba54-89c7-4d0c-aad02dc519b4.jpeg)  
  
参考教材　2018.11.9 FOSS4G 2018 Tokyo ハンズオン「QGIS 初級」の資料　  
https://speakerdeck.com/yukosame/qgis-chu-ji-opundetadedi-tu-wozuo-rou-and-qgis-3d-ti-yan  
  
  
