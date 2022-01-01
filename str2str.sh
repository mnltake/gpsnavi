#! /bin/sh
cd /home/pi/RTKLIB/app/str2str/gcc
sudo ./str2str -in serial://ttyACM0:115200 -out ntrips://:BETATEST@rtk2go.com:2101/[MountID]

