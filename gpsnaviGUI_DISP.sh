#!/bin/sh
cd /home/pi/gpsnavi
/usr/bin/lxterminal -e /home/pi/gpsnavi/userver-navi.py &
sleep 15
/usr/bin/lxterminal -e sudo python3 /home/pi/gpsnavi/gpsnavi-cli.py 
