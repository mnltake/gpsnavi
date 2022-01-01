#!/bin/sh
cd /home/pi/gpsnavi
/home/pi/lv_micropython/ports/unix/micropython /home/pi/gpsnavi/userver-navi.py &
/usr/bin/lxterminal -e sudo python3 /home/pi/gpsnavi/gpsnavi-UBX.py
