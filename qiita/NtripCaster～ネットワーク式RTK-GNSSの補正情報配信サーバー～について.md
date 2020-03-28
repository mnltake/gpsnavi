# 　はじめに  
インターネット回線を利用したRTK-GNSSの[Ntrip](https://ja.wikipedia.org/wiki/Ntrip)方式には  
1. Ntrip Server（基準局）  
2. Ntrip Client (移動局）  
3. Ntrip Caster　（配信サーバー）  
が必要です。  
![接続図ntrip.jpg](/image/f8cc9f95-dbd5-5f66-a2ab-783badedf0fb.jpeg)  
画像引用元：https://toragi.cqpub.co.jp/tabid/865/Default.aspx  
  
基準局・移動局についてはQiitaなどネット上に情報がありWindowsPC、ラズベリ－パイ、ESP32などでの方法が詳しく紹介されています。  
参考  
[Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）](https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その１）.md)  
[F9Pで基地局](https://qiita.com/yasunori_oi/items/a6cf9323fc2c94acd22a)  
[ESP32でRTCM3受信機](https://qiita.com/yasunori_oi/items/1af14c548d75041c64e2)  
  
ここではNtrip Casterについて私の知っている限りでまとめてみました。  
  
# 　rtk2go.com  
http://www.rtk2go.com/  
○　無料で使える  
**(注意)2019/9 以降仕様が変更となメールアドレスの登録が必須となりました**  
　http://www.rtk2go.com/new-reservation/  
　**以前のパスワード「BETATEST」は使えません**  
  
●　基準局は公開  
　自宅に基準局を立てている場合、分かる人には住所をcm精度で特定されます。　  
  
●　安定性に難あり　  
　個人的経験ですが繋がらないときが半日ぐらい続いたり、送られてくるデータも不連続だったりしたことがありました。そもそも半径10kmしか使えないのにわざわざ海外のサーバーまで往復させるのはトラフィックの無駄じゃないかと  
  
***とりあえず試しに使ってみたい人にはおすすめ***  
  
  
# 　自前のWindowsサーバーでSNIPを利用  
https://www.use-snip.com/  
rtk2goを開設しているところが作っているソフトウェアです  
多機能の有料版もありますが無料の評価版もあります。  
詳しくは最近発売されたこの本を参考にしてください。  
  
**『SNIPによるRTK基準局開設・運用入門』コロナ社**　  
　https://www.coronasha.co.jp/np/isbn/9784339009293/  
  
○無料（評価版）で使える  
○自宅/会社のWindowsPCで使える（Ubuntu版もあり）  
　英語ですがGUI画面で設定可能  
  
○基準局は非公開も可能  
  
●外部からアクセスするにはポートマッピングが必要  
　プロバイダー等によっては出来ない場合も、またセキュリティーも自己責任で  
  
***電気代だけでランニングコストがかからない。***  
  
# 　AgriBus-Caster　を利用  
https://agri-info-design.com/agribus-caster/  
農業技術情報社の農業用トラクタガイダンスアプリ「AgriBus-NAVI」の有料サービスです  
  
○日本語サポートあり  
○基準局は非公開  
● ~~年額6000円（2019.12現在）~~  年額12000円 ／月額1200円（2020現在）のスタンダードプラン購読が必要  
  
***AgriBus-NAVIを使用してる方にはおすすめ***  
  
  
# 　有料VPSを利用  
　**さくらVPS**　　https://vps.sakura.ad.jp/ (585円/月～）  
　**Amazon Lightsail** https://aws.amazon.com/jp/lightsail/ （3.5ドル/月～）  
などに立てたサーバーにフリーのNtrip Casterソフトを動かす方法です。  
rtcmの場合、数kbpsのデータストリームを１～数台の移動局に配信するだけなので最低クラスのプランで十分です  
  
Amazon Lightsailについては丁度いい記事があったのでこちらをご覧ください  
[[動画あり] たった5分でAWSに月額3.5ドルの格安VPNサーバーを構築する方法](https://qiita.com/alfa/items/6ae09a48769c5f6bf5e9)  
[AWS Lightsailでインスタンスを作成する](https://qiita.com/SSMU3/items/8abc581fb8fcff97de73)  
記事ではDebianとUbuntuですが今回はCentOSでの方法を紹介します。  
yum　と　apt-get の違いだけで多分いけると思います。  
```$ su```
```$ yum update -y```  
```$ yum install git gcc nano```

```$ git clone git@github.com:mnltake/ntripcaster.git```  
https://github.com/roice/ntripcaster　  
からForkしました。作者はBKGとありますがGNUライセンスと書いてあるので自由に使っていいのでしょう（多分）。インストールの方法はREADME.txtに書いてあります  
  
```$ cd ntripcaster/ntripcaster0.1.5/```
```$ ./configue```  
```$ make```
```$ make install```  
```$ cd /usr/local/ntrincaster/conf```
```$ nano ntripcaster.conf.dist```  
サーバー名、最大接続数、Ntrip Server接続用パスワード、サーバーIP/ポート、Ntrip Caster用パスワードを設定して「ntripcaster.conf」に名前を変えて保存  
  
```$ nano sourcetable.dat.dist```
こちらを参考に sourcetable　を書き換えて「sourcetable.dat」に名前を変えて保存
（公開しないなら適当でも）
https://software.rtcm-ntrip.org/wiki/STR

```$ cd  usr/local/ntrincaster/bin```  
```$ ./ntripcaster```

設定したポート（例：2101）をAmazon LightsailのFirewall設定で開けて必要ないポートは閉じておきます。


○基準局は非公開も可能
○自宅のルーターでポート開放ができない場合でも可能
○安定
~~Amazonのサーバーがダウンすることなんかそうそうないよね~~
●有料
　ただし月400円弱で電気代やセキュリティーの心配はない

***安定重視で仕事で使いたい方におすすめ***

# （追記）自宅ラズパイサーバー
NtripCasterを使わなくても自宅のポートが開けて外部から接続できるのであればRTKLIBのstr2strで
[基準局]　-out tcp server  [移動局]　-in tcp client で接続できます。

また移動局のアプリでNtrip Clientの入力しかない場合はラズパイの中に上で紹介した[ntripcaster0.1.5](https://github.com/roice/ntripcaster　)はRaspbianでも動くはずなので、基準局のラズパイにNtrip Server(str2str）とNtrip Casterを入れて外部からNtrip Clientとして接続できます（未検証）
**参考**
[F9PまたはM8tを搭載したRaspberry上のNtripBase](https://cerea-forum.de/forum/index.php?thread/105-ntripbase-auf-dem-raspberry-mit-f9p-oder-m8t/&pageNo=1)
https://cerea-forum.de/ より

## （追記の追記）##
教えてもらったところによるとRTKLIBのstr2str単体にもNtripCasterの機能があるようです。
開発版のrtklib_2.4.3のなかにスクリプトが入ってますのでsrctbl.txtも適宜書き換えて使えます（未検証）
https://github.com/tomojitakasu/RTKLIB/blob/rtklib_2.4.3/app/str2str/run_cast.sh
