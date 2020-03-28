  
ラズベリーパイ３BでフルカラーシリアルLED NeoPixel(ws2812B)を以前使えたはずだが  
Raspbian（Buster）に代えてからつまずいたことがあったのでメモしておきます。  
  
  
  
# 配線  
https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring  
ラズパイは3.3V信号 　Neopixelは5V信号のため  
74AHCT125レベルコンバータを使う方法とダイオードを使う方法が紹介されている  
ダイオードを使う方法で試してみる。信号線はGPIO18（PWM0)  
**Raspberry Piの5V出力から数個を超えるNeoPixelsに電力を供給しない**  
守らないと壊れます（壊しました）  
  
# Raspberry Pi　ライブラリ  
**https://github.com/jgarff/rpi_ws281x  
Userspace Raspberry Pi PWM library for WS281X LEDs**  
  
`git clone https://github.com/jgarff/rpi_ws281x`  
scons が要るというのでインストール（makeの代わりのようなものらしい）  
`sudo apt-get install scons`  
`cd rpi_ws281x`  
`scons`  
  
~~でいいはずだが~~  
~~‘makedev’が定義されてないとエラーが出た~~  
~~://www.raspberrypi.org/forums/viewtopic.php?t=250220~~  
  
~~mailbox.c を編集して **\#include \<sys/sysmacros.h>**を追加~~  
~~`nano mailbox.c`~~  
~~再び~~  
~~`scons`~~（不要でした）  
成功!  
  
# python　ライブラリ  
**https://github.com/rpi-ws281x/rpi-ws281x-python  
Python library wrapping for the rpi-ws281x library**  
`  
sudo pip3 install rpi_ws281x  
git clone https://github.com/rpi-ws281x/rpi-ws281x-python  
cd rpi-ws281x-python/example  
chmod 755 *.py  
sudo python3 strandtest.py  
`  
成功!（sudo が必要）  
