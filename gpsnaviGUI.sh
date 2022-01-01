#!/bin/sh
DISPLAY=:0 micropython /home/pi/gpsnavi/userver-navi.py &
sleep 5
/usr/bin/lxterminal -e sudo python3 /home/pi/gpsnavi/gpsnavi-cli.py &
