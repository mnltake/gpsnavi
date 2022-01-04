#!/bin/sh
cd /home/pi/gpsnavi

sleep 1
/usr/bin/lxterminal -e sudo python3 /home/pi/gpsnavi/gpsnavi-cli.py
