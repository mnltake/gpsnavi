  
# 目標  
トラクターや田植え機にGPS（GNSS)を使い直進走行をアシストするガイダンスを作ります。  
半年ほど前に雑誌「トランジスタ技術」を手にしてからプログラムも電子工作もほぼ未経験から  
独学で苦労して作りましたが今シーズンの田植え作業で実用的になるのが実証できたので  
紹介したいと思います。  
将来的にはステアリングモーターを使い自動走行までできるようになりたいです。  
# デモ動画　（2018.11.13更新）  
[YouTube 自作RTK-GPS　ガイダンス　デモ ](https://www.youtube.com/watch?v=y36dDZJX1TM&feature=youtu.be)(注：音が出ます）  
# 応用編　（2019.11.1更新）  
自作直進アシストコンバイン  
[(1)](https://www.youtube.com/watch?v=WsRx6_l2uik) [(2)](https://www.youtube.com/watch?v=qkLJFR_Ap_U) [(3)](https://www.youtube.com/watch?v=2urhKWN__Ns) [(4)](https://www.youtube.com/watch?v=pLQ9PLHsBcY)  
  
# 準備するもの  
・トランジスタ技術2018年1月号  
http://toragi.cqpub.co.jp/tabid/865/Default.aspx  
・（2019/1/16追記）**トランジスタ技術2019年2月号  
　別冊RTKスタートアップ・マニュアルにu-centerとRTKLIBの使い方について詳しく解説あり**  
  
・Ublox NEO-M8P-0モジュール搭載(RTKエンジン，RAW対応)，GPS/Beidouアンテナ付き  
トラ技RTKスタータキット移動局用【TGRTK-B】￥21600　X　2台  
http://shop.cqpub.co.jp/hanbai/books/I/I000239.html  
  
（実は私は基準局用のTGRTK-Aを購入して基準局に使用していますが、RTKLIBで測位するのなら移動局用のTGRTK-Bを2台でも可能なのではないかと。実際検証したわけではないので間違っていたらご指摘ください）  
  
・GPSアンテナ　Tallysman社 TW2710　￥11117　  
https://www.digikey.jp/product-detail/ja/tallysman-wireless-inc/33-2710-00-5000/1526-1014-ND/4862786  
付属のアンテナではなかなかFIXしませんでしたが移動局だけこれに替えたら  
体感で７～8割程度はFIXするようになりました  
**(追記）基準局もTW2710に変えたら95%以上FIXするようになりました（5km以内）**  
  
・raspberrypi3　ｘ　2台  
・スマートフォン（テザリング機能付き）  
・USB電源ポート(12v -> 5v 2.4A以上）  
https://www.monotaro.com/p/1999/7653/  
・電子工作部品（USBケーブル、LED、抵抗、キーパッドなど）  
  
諸々で基準局＋移動局1台で10万円以内でできます（市販品ではRTK-GPSガイダンスで100万円以上、精度20cm程度のDGPSで数10万円します）  
  
（＊NEO-M8Pの代わりにNEO-M8T（$75）  
https://www.csgshop.com/product.php?id_product=205  
RaspberryPi3の代わりにRaspberryPiZEROWを使えば5万程度で可能。下記参考）  
  
**(2019/5 追記）**  
市販品でも安価な受信機が発売されだしており例えば農業情報設計社のAgriBus-GMiniだと  
59,800円（税別）＊２台　＋　Androidタブレット　でRTK-GPSガイダンスが使えるようになりました。  
https://agri-info-design.com/  
https://agri-info-design.com/agribus-gmini/  
  
# 参考リンク  
http://gpspp.sakura.ne.jp/index.shtml  
RTKLIBの作者高須知二先生のサイト  
マニュアルhttp://www.rtklib.com/prog/manual_2.4.2.pdf  
と日記・備忘録には情報が満載です  
http://www.rtk2go.com/  
無料で使えるNTRIP　Caster を提供しています  
  
  
# 概念図  
![net.png](/image/b15e75db-df77-4777-6e04-cb0534e14e2d.png)  
  
  
# 基準局（Base）  
M8Pの出力はu-centerでGNSS>GPS+BeiDou＋QZSS  
MSG＞  
02-13　RXM-SFRBX  
02-15 RXM-RAWX  
がUSBから出力されるようにします（詳しくはトラ技2018年1月号と特設サイトを参照）  
次にRaspberry Piでの設定について  
RTKLIBのインストールの仕方はこちらに詳しくあります  
http://toragi.cqpub.co.jp/Portals/0/support/junior/article/2017/1704gnss.html  
基準局で使用するのは　***str2str*** コマンドラインのNTRIP　server プログラムです  
使い方はマニュアル2.4.2の99ページにあります  
私の設定では以下の実行ファイルを作成し実行権限を付けておきます  
  
**str2str.sh**  
```sh:str2str.sh
# ! /bin/sh
cd /home/pi/RTKLIB/app/str2str/gcc
./str2str -in serial://ttyACM0:115200 -out ntrips://:BETATEST@rtk2go.com:2101/[MountID] 
```  
  
[MountID]は適宜置き換えてください  
  
こちらを参考にsystemctl で自動実行できるようにしておきます  
http://hendigi.karaage.xyz/2016/11/auto-boot/  
  
  
# 移動局（Rover)  
同じく車載用のRaspberry PiにもRTKLIBをインストールします  
移動局に使うのは　***rtkrcv*** コマンドラインのrtk測位プログラムです  
.confファイルで設定をしますが私の例は以下で参考にしてください  
[MountID],基準局位置の緯度経度高度（ant2-pos*)は適宜置き換えてください  
入力は基準局がスマホ経由のntripsvr、移動局はserial(USB)でそれぞれubx形式  
出力は一つがローカルホストの：52001ポートに基準局からの東西南北の距離（enu)  
もう一つはfileに緯度経度（llh)を0.2秒ごと（5Hz)に出します  
  
  
  
  
```my.conf
 # rtkrcv options for rtk 
console-passwd     =admin
console-timetype   =gpst      # (0:gpst,1:utc,2:jst,3:tow)
console-soltype    =dms        # (0:dms,1:deg,2:xyz,3:enu,4:pyl)
console-solflag    =1          # (0:off,1:std+2:age/ratio/ns)
inpstr1-type       =serial     # (0:off,1:serial,2:file,3:tcpsvr,4:tcpcli,7:ntripcli,8:ftp,9:http)
inpstr2-type       =ntripcli   # (0:off,1: serial,2:file,3:tcpsvr,4:tcpcli,7:ntripcli,8:ftp,9:http)
inpstr3-type       =off        # (0:off,1:serial,2:file,3:tcpsvr,4:tcpcli,7:ntripcli,8:ftp,9:http)
inpstr1-path       =ttyACM0:115200:8:n:1:off
inpstr2-path       =rtk2go.com:2101/[MountID]
inpstr3-path       =
inpstr1-format     =ubx       # (0:rtcm2,1:rtcm3,2:oem4,3:oem3,4:ubx,5:ss2,6:hemis,7:skytraq,8:sp3)
inpstr2-format     =ubx     # (0:rtcm2,1:rtcm3,2:oem4,3:oem3,4:ubx,5:ss2,6:hemis,7:skytraq,8:sp3)
inpstr3-format     =rtcm3      # (0:rtcm2,1:rtcm3,2:oem4,3:oem3,4:ubx,5:ss2,6:hemis,7:skytraq,8:sp3)
inpstr2-nmeareq    =off        # (0:off,1:latlon,2:single)
inpstr2-nmealat    =          # (deg)
inpstr2-nmealon    =          # (deg)
outstr1-type       =tcpsvr      # (0:off,1:serial,2:file,3:tcpsvr,4:tcpcli,6:ntripsvr)
outstr2-type       =file   # (0:off,1:serial,2:file,3:tcpsvr,4:tcpcli,6:ntripsvr)
outstr1-path       =:52001
outstr2-path       =/home/pi/RTKLIB/rtklog/%Y%m%d_%h%M_sol.pos
outstr1-format     =enu        # (0:llh,1:xyz,2:enu,3:nmea)
outstr2-format     =llh      # (0:llh,1:xyz,2:enu,3:nmea)
logstr1-type       =off        # (0:off,1:serial,2:file,3:tcpsvr,4:tcpcli,6:ntripsvr)
logstr2-type       =off        # (0:off,1:serial,2:file,3:tcpsvr,4:tcpcli,6:ntripsvr)
logstr3-type       =off        # (0:off,1:serial,2:file,3:tcpsvr,4:tcpcli,6:ntripsvr)
logstr1-path       =/home/pi/RTKLIB/rtklog/%Y%m%d%h%M_rov.log
logstr2-path       =/home/pi/RTKLIB/rtklog/%Y%m%d%h%M_base.log
logstr3-path       =cor_%Y%m%d%h%M.log
misc-svrcycle      =10         # (ms)
misc-timeout       =20000      # (ms)
misc-reconnect     =20000      # (ms)
misc-nmeacycle     =5000       # (ms)
misc-buffsize      =32768      # (bytes)
misc-navmsgsel     =all      # (0:all,1:rover,1:base,2:corr)
misc-startcmd      =./rtkstart.sh
misc-stopcmd       =./rtkshut.sh
file-cmdfile1      =../../../data/ubx_m8p_rov_bds_5hz.cmd
file-cmdfile2      =../../../data/ubx_m8p_ref_bds_1hz.cmd
file-cmdfile3      =
pos1-posmode       =kinematic # (0:single,1:dgps,2:kinematic,3:static,4:movingbase,5:fixed,6:ppp-kine,7:ppp-static)
pos1-frequency     =l1      # (1:l1,2:l1+l2,3:l1+l2+l5)
pos1-soltype       =forward    # (0:forward,1:backward,2:combined)
pos1-elmask        =15         # (deg)
pos1-snrmask_L1    =40,40,40,40,40,40,40,40,40    # (dBHz)
pos1-dynamics      =off        # (0:off,1:on)
pos1-tidecorr      =off        # (0:off,1:on)
pos1-ionoopt       =brdc       # (0:off,1:brdc,2:sbas,3:dual-freq,4:est-stec)
pos1-tropopt       =saas       # (0:off,1:saas,2:sbas,3:est-ztd,4:est-ztdgrad)
pos1-sateph        =brdc       # (0:brdc,1:precise,2:brdc+sbas,3:brdc+ssrapc,4:brdc+ssrcom)
pos1-exclsats      =C02           # (prn ...)
pos1-navsys        =49          # 49 (1:gps+2:sbas+4:glo+8:gal+16:qzs+32:comp)
pos2-armode        =fix-and-hold # (0:off,1:continuous,2:instantaneous,3:fix-and-hold)
pos2-gloarmode     =off        # (0:off,1:on,2:autocal)
pos2-bdsarmode     =on
pos2-arthres       =3
pos2-arthres1      =0.9999
pos2-arthres2      =0.25
pos2-arthres3      =0.1
pos2-arthres4      =0.05
pos2-arlockcnt     =0
pos2-arelmask      =0          # (deg)
pos2-aroutcnt      =5
pos2-arminfix      =10
pos2-slipthres     =0.05       # (m)
pos2-maxage        =30         # (s)
pos2-rejionno      =30         # (m)
pos2-niter         =1
pos2-baselen       =0          # (m)
pos2-basesig       =0          # (m)
out-solformat      =llh        # (0:llh,1:xyz,2:enu,3:nmea)
out-outhead        =off         # (0:off,1:on)
out-outopt         =off        # (0:off,1:on)
out-timesys        =gpst       # (0:gpst,1:utc,2:jst)
out-timeform       =tow        # (0:tow,1:hms)
out-timendec       =3
out-degform        =deg        # (0:deg,1:dms)
out-fieldsep       =
out-height         =geodetic # (0:ellipsoidal,1:geodetic)
out-geoid          =internal   # (0:internal,1:egm96,2:egm08_2.5,3:egm08_1,4:gsi2000)
out-solstatic      =all        # (0:all,1:single)
out-nmeaintv1      =0          # (s)
out-nmeaintv2      =0          # (s)
out-outstat        =off        # (0:off,1:state,2:residual)
stats-errratio     =100
stats-errphase     =0.003      # (m)
stats-errphaseel   =0.003      # (m)
stats-errphasebl   =0          # (m/10km)
stats-errdoppler   =1          # (Hz)
stats-stdbias      =30         # (m)
stats-stdiono      =0.03       # (m)
stats-stdtrop      =0.3        # (m)
stats-prnaccelh    =1          # (m/s^2)
stats-prnaccelv    =0.1        # (m/s^2)
stats-prnbias      =0.0001     # (m)
stats-prniono      =0.001      # (m)
stats-prntrop      =0.0001     # (m)
stats-clkstab      =5e-12      # (s/s)
ant1-postype       =llh        # (0:llh,1:xyz,2:single,3:posfile,4:rinexhead,5:rtcm)
ant1-pos1          =0          # (deg|m)
ant1-pos2          =0          # (deg|m)
ant1-pos3          =0          # (m|m)
ant1-anttype       =
ant1-antdele       =0          # (m)
ant1-antdeln       =0          # (m)
ant1-antdelu       =0          # (m)
ant2-postype       =llh        # (0:llh,1:xyz,2:single,3:posfile,4:rinexhead,5:rtcm)
ant2-pos1          =34.xxxxx  # (deg|m)
ant2-pos2          =136.xxxxx # (deg|m)
ant2-pos3          =xx.xxx	   # (m|m)
ant2-anttype       =
ant2-antdele       =0          # (m)
ant2-antdeln       =0          # (m)
ant2-antdelu       =0          # (m)
misc-timeinterp    =off        # (0:off,1:on)
misc-sbasatsel     =0          # (0:all)
file-satantfile    =../../../data/igs05.atx
file-rcvantfile    =../../../data/igs05.atx
file-staposfile    =../../../data/station.pos
file-geoidfile     =
file-dcbfile       =../../../data/P1C1_ALL.DCB
file-tempdir       =../../../data/temp
file-geexefile     =
file-solstatfile   =
file-tracefile     =
```  
  
実行ファイルを作成し実行権限を付けておきます  
  
**rtkrcv.sh**  
```sh:rtkrcv.sh
# !/bin/sh
cd /home/pi/RTKLIB/app/rtkrcv/gcc/
./rtkrcv  -o /home/pi/RTKLIB/app/rtkrcv/my.conf -s -d /dev/tty0
```  
  
同じく自動起動できるようにしておきます  
（このとき　-d /dev/tty0　がないとうまくいきません）  
  
# 材料一覧（2019/1/16追記）#  
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
|電線（インターホン用0.65mmx 4芯　10m）|720|ホームセンター|  
|**【オプションBluetooth出力】**||  
|RN-42使用　Bluetooth無線モジュール|2222|http://akizukidenshi.com/catalog/g/gK-07378/|  
|必要に応じてUSB延長ケーブル、スマホホルダー||  
あとスマホ本体、データ通信sim(~2GB/月）  
  
  
[続く](https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その２）.md)  
  
