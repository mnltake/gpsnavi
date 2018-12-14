#!/bin/sh
cd /home/pi/RTKLIB/app/rtkrcv/gcc/
./rtkrcv  -o /home/pi/gpsnavi/my.conf -s -d /dev/tty0 -m 52002
