# はじめに  
この記事は私が2019年に苦闘した記録ですが技術的に有用な情報はあまりないのであしからず。  
  
(2020.2.6)追記  
なんとかフィールドテストまでたどり着きました。実作業で使えるかはこれからです。  
  
# ここまでの歩み（2018年）  
[最初の記事](https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）.md)に書いたようにUblox-M8Pを手にし初めてRTKをしたのが2年前。4ヶ月ぐらいかけて直進ガイダンスを作り春の田植作業に使用。有用性を感じてQittaに投稿したのが6月。秋の農繁期を終えて11月に[FOSS4G](https://www.osgeo.jp/)という地図好きの集まりがあると知り東京までいって刺激を受けてくる。（この頃から[Twitter](https://twitter.com/mnlt18)始める）  
　[ボタン一つでAB基準線を呼び出したり](https://github.com/mnltake/gpsnavi/blob/master/GPSの位置からシェイプファイルの属性データを取り出す.md)自分の使いたい機能を付けて満足しつつあるときに、  
[AgOpenGPS](https://agopengps.jimdosite.com/) (以下AOG)というソフトをカナダの農家が作成してオープンソースで公開していることを知る。自作でモーターを取り付け自動操舵までやってる！！  
  
# 2019年1月～3月  
自作ガイダンスでトラクター作業をしつつ [帽子にLEDを付けてみたり] (https://twitter.com/mnlt18/status/1093017845347151872) ,　[傾斜補正をつけてみたり](https://twitter.com/mnlt18/status/1089829812624011264)　しているが自動操舵の方は手つかず。  
巷ではF9Pを手にした方の報告が上がるようになり指をくわえてみている。  
  
# 4月～5月  
春の農繁期。自作の他にAOGも併用して使い方がだんだんわかってくる。[セクションコントロール](https://twitter.com/mnlt18/status/1127934965130285056) や、[GPSでお絵かき](https://twitter.com/mnlt18/status/1130049508732227584)など。  
忙しさの勢いでF9Pを一つだけ買うが[まだ2周波の威力を試せず](https://twitter.com/mnlt18/status/1129358244428693504)  
  
# 6月～8月  
[F9Pの使い方を覚えたり](https://github.com/mnltake/gpsnavi/blob/master/続・Raspberry Piでcm精度のRTK-GPSガイダンスの制作（2周波へ向けて）.md),  
[自分用のNtripCasterを立ち上げたり](https://github.com/mnltake/gpsnavi/blob/master/NtripCaster～ネットワーク式RTK-GNSSの補正情報配信サーバー～について.md)  
時間ができ、またAOGのフォーラムを読んでいると自動操舵用のPCBの設計まで公開していた。  
そのなかからESP32,IMU,モータードライバ,A/Dコンバータ、Ethernet,リレー,F9Pコネクタ…[全部乗せの基板のガーバーデータが公開されているのを知る](https://github.com/doppelgrau/esp32-f9p-io-board)  
  
当時[fusionpcb](https://www.fusionpcb.jp/)で基板製造＋部品実装5枚で実装代無料のキャンペーンが行われていたこともあり、無謀にも初のPCBで表面実装部品点数120以上/枚を発注  
  
# 9月～10月  
結局発注から到着するまで一月半かかり秋の農繁期に入ってしまったので基板は手つかずのまま。  
[コンバインにガイダンスをつけて](https://twitter.com/mnlt18/status/1169935136160247808)使ってみたら[中割作業に役立った](https://twitter.com/mnlt18/status/1168857472481652738)。  
また[降水予測機能を付けて](https://twitter.com/mnlt18/status/1166272314100502529)助かったり[騙されたり](https://twitter.com/mnlt18/status/1179229837938036738)  
台風で稲刈りが出来ない日に試しに[コンバインの自動操舵を付けてみたら意外にスムーズに動いた！](https://twitter.com/mnlt18/status/1183230419296124928)  
  
# 11月～12月  
稲刈りも終わりいよいよトラクタの自動操舵に手を付ける。  
ざっくりと[AOGの仕組み](http://agopengps.gh-ortner.com/doku.php#how_agopengps_works)を説明すると  
  
  
1.　GPS受信機からNMEAを受信(AOGからRTCMを送信する機能もあり）  
2.　AutosteerPCBからRoll,Headingを受信　  
3.　AOG本体はWindowsPC上で動くC#で書かれていて、ステアリングの目標角を計算しAutosteerPCBに送信。  
4.　AutosteerPCB上のAruduinoまたはESP32 で受け取った**目標角(steerAngleSetPoint)**と、ポテンショメータとA/Dコンバータで計測した前輪の**操舵角（steerAngleActual）**の差がゼロになるようにPID制御（実際はP制御のみ）でモータードライバのPWM値を決めハンドルに取り付けたDCモーターを回す。  
  
1.2.4.を一つのESP32 で動かそうとマルチコアだとか非同期UDP通信とか（AsyncUDP）とか、入門書には書いてないようなものを訳も分からずコピペで動かそうとする。[一瞬うごいた気がした](https://twitter.com/mnlt18/status/1190083761498492928)が安定には程遠く数十秒で再起動を繰り返し原因がつかめず。  
  
　それはひとまず置いおいて、並行してモーター取り付けのハードウェアにも取り掛かる。[とりあえず置いてみただけでは](https://twitter.com/mnlt18/status/1192253791912939521)強度的にも精度的にも使い物にならないので海外のサイトを参考に探していたら、[ドイツのフォーラムで3Dプリンタ用のギア図面を公開している人がいる！](https://cerea-forum.de/filebase/index.php?file/80-zahnrad-halterung-valtra/)  
　  
　3DCADソフト[Fusion360](https://www.autodesk.co.jp/products/fusion-360/)の基本的な使い方を覚えて（つくづくフリーソフトが好きだな）3万以下の３DプリンターEnder-3 Proを購入。  
ABS樹脂の層割れや反りなど初心者の失敗を一通り経験したあと、PETG樹脂で [ハードは結構うまく出来上がった！](https://twitter.com/mnlt18/status/1210126329456152576)  
  
　そして現時点。AOG-ESP(wifi_UDP)の通信部のエラーがまだ未解決。ならばと自作ラズパイとESPにUSB接続で動かせないか、と考えてみたがこれも[制御アルゴリズムを一から勉強しないと難しそう](https://twitter.com/mnlt18/status/1212144493777965057)。  
  
　もうひとつの手はせっかく作ったESPの基板を諦めて[Aruduinoではじめから作り直す。](https://github.com/farmerbriantee/AgOpenGPS/tree/master/PCB/AutoSteerPCB_Gerber)こちらはAOGの作者本人が作ったのでスケッチも改変せずにそのままで動くはず（？）  
  
さて2020年には完成するでしょうか？　　... to be continued  
  
# 2020年1月～  
　上の記事書いて読み直していると気づいた点が問題はwifi_UDPの通信部が問題ならばシリアル（USB)でAOGと接続すればよいのでは？  
　[ArduinoNANOを使ったスケッチ](https://github.com/farmerbriantee/AgOpenGPS/tree/master/ArduinoCode/AutosteerPCBv2)ではUSBとEthernet_UDP接続の2つの方法が選べるようになっている。これをESP32に移植。int型がArduinoでは16bit,ESP32では32bitであること。millis()の戻り値をunsigned longで受け取ることなどにつまずきつつなんとか完成。  
　さらに[BluetoothSerialライブラリ](https://github.com/espressif/arduino-esp32/tree/master/libraries/BluetoothSerial)を使えばタブレットのUSBポートを使わずに無線で接続できた（たまに切れることもあるが）  
https://github.com/mnltake/AutosteerPCBv_esp32  
  
　またモーターも２個搭載することでトルク不足による発熱も抑えられ連続運転も可能になった。  
https://github.com/mnltake/Steer-motor-3D-Print-for-ISEKI/  
[路上での試運転](https://twitter.com/mnlt18/status/1225253654082359298)は成功したのでいよいよ圃場作業での実戦に挑む！  
  
  
  
