#!/bin/sh

cd /home/pi/RTKLIB/app/str2str/gcc/

./str2str  -in ntrip://rtk2go.com:2101/[MountID] -out serial://ttyUSB0:115200
