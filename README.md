RTK-GPS/GNSS guidance for agriculture tractor  by python code

powered by RTKLIB
https://github.com/tomojitakasu/RTKLIB

How to use

Raspberry Piでcm精度のRTK-GPSガイダンスの制作

https://qiita.com/m_take/items/06892a8e25aa577e8455

https://qiita.com/m_take/items/da9119a9dc9660f96227

Demo clip

https://www.youtube.com/watch?v=y36dDZJX1TM&feature=youtu.be

Auto start settiing

https://github.com/mnltake/gpsnavi/blob/master/autostart_setting.txt

**Only guidance not auto-pilot (yet)**

**Only CUI not GUI**

**Only straight line not curve** 

**Only 2D field not 3D**

BUT

**Any Tablet/Smartphone(windows,android,iOS..)　can use,** because it's used only VNC(Virtual Network Computing)Viewer and 3G/LTE tethering.Everything is calculated on Raspberry Pi.

**No USB port need.You can use for charge**

AND

**Software costs are free!!**
**You can change as you like**

![image](https://github.com/mnltake/gpsnavi/blob/master/image.png)

#材料一覧#

| 品名             | 参考価格円 （税抜き送料別） |        入手先        |
|:-----------------|------------------:|:------------------:|
|**【受信機】**|||
|M8P　*　2台|40000|http://shop.cqpub.co.jp/hanbai/books/I/I000239.html|
|GPSアンテナ（1周波）　Tallysman社 TW2710　*2台|22576|https://www.digikey.jp/product-detail/ja/tallysman-wireless-inc/33-2710-00-5000/1526-1014-ND/4862786|
|[参考]M8T　　*　2台|16500（1$=110円として）|https://www.csgshop.com/product.php?id_product=205|
|[参考]F9P（2周波、アンテナ付き）　＊　2台|57000　（1ユーロ=125円として）| https://www.ardusimple.com/product/simplertk2b-basic-starter-kit-ip65/|
|**【ラズベリーパイ】**|||
|Pi ZeroWH　（base用）#ZeroWも可|1675|https://raspberry-pi.ksyic.com/main/index|
|Pi3 B (rover用）#Pi3 B+までは必要ない　Pi3 A+が発売されたらもう少し安くなるかも |4000|https://raspberry-pi.ksyic.com/main/index|
|microSDカード　8GB以上　*2枚|1500|https://raspberry-pi.ksyic.com/main/index|
|USB電源アダプター 5V/1A（base用）|800|https://raspberry-pi.ksyic.com/main/index|
|DC-DC降圧　（rover用）|395|http://www.aitendo.com/product/16566|
|12Vコネクタ、ヒューズ|||
|USBケーブル＊4、鍋の蓋（グランドプレーン用）＊2、プラケース＊2|800|百均|
|**【rover操作用】**||
|薄膜パネルスイッチ（3ｘ4　navi操作用）|248|http://www.aitendo.com/product/4736|
|薄膜パネルスイッチ（シャットダウンスイッチ用）|195|http://www.aitendo.com/product/11784|
|リードスイッチ（ポジションレバー用）|100|http://www.aitendo.com/product/17890|
|**【オプション傾斜補正】**||
|MPU-6050搭載3軸加速度/ジャイロモジュール|475|http://www.aitendo.com/product/9549|
|**【オプションLED表示】**||
|ユニバーサル基板（Pi)|165|http://www.aitendo.com/product/12108|
|LED表示器|300|http://www.aitendo.com/product/16891|
|ユニバーサル基板（65X37）|70|http://www.aitendo.com/product/14535|
|プラケース [C70X42X18]|100|http://www.aitendo.com/product/11214|
|ターミナルブロック（5.08）3P *3個|90|http://www.aitendo.com/product/10098|
|抵抗　200Ω、ピンソケット、ピンヘッダ、ジャンパー線|300||
|電線（インターホン用0.65mmx 4芯　10m）|2000|ホームセンター|
|**【オプションBluetooth出力】**||
|RN-42使用　Bluetooth無線モジュール|2222|http://akizukidenshi.com/catalog/g/gK-07378/|
|必要に応じてUSB延長ケーブル、スマホホルダー||

配線図
![image](https://github.com/mnltake/gpsnavi/blob/master/Pi_gpsnavi.png)
