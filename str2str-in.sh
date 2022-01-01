#!/bin/sh

cd /home/pi/RTKLIB/app/str2str/gcc/
sudo ./str2str -in ntrip://guest:guest@52.194.74.83:2101/HIGASHIURA -out serial://ttyAMA0:115200
#./str2str  -in ntrip://rtk2go.com:2101/Meijo-T-RTCM3 -out serial://ttyUSB0:115200
