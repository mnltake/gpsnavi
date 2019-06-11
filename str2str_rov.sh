#! /bin/sh
cd /home/pi/RTKLIB/app/str2str/gcc
./str2str -in ntrip://guest:guest@52.194.74.83:2101/HIGASHIURA -out serial://ttyACM0:115200
./str2str -in serial://ttyUSB0:115200 -out tcpsvr://:52007
