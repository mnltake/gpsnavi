#!/bin/sh
cd /home/pi/gpsnavi
DISPLAY=:0 /home/pi/lv_micropython/ports/unix/micropython /home/pi/gpsnavi/userver-navi.py &
sleep 5
/usr/bin/lxterminal -e sudo python3 /home/pi/gpsnavi/gpsnavi-cli.py 
