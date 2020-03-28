# 目的  
***LLH***（緯度Lat(deg),経度Lon(deg),高さ Height(m))座標から  
***ENU***（東East(m),北North(m),上Up(m):基準点からの相対距離)座標への変換。  
  
# 結論  
***Pymap3d***を使う。  
  
参考  
緯度経度、ECEF系、方位角・仰角などの座標変換に便利なプログラムPyMap3d  
https://qiita.com/ina111/items/6e3c4d85036fd993d23c  
pymap3d.enu module  
https://scivision.github.io/pymap3d/enu.html  
  
```
pip3 install pymap3d
```  
numpyがうまくインポートできなかったときは一度アンイストールしてからapt-get で  
  
```
pip3 uninstall numpy
sudo apt-get install python3-numpy
```  
  
  
  
**llh2enu.py**  
```python:llh2enu.py
import pymap3d as pm
base = [base_lat ,base_lon ,base_h] #deg,deg,m
rover =[rover_lat ,rover_lon ,rover_h ] #deg,deg,m
rover_enu = pm.enu.geodetic2enu(rover[0] ,rover[1] ,rover[2],base[0] ,base[1] ,base[2])#m,m,m
```  
# 何がしたいのか？  
話は以上ですが何に使いたかったのかと言うと  
  
1.[llh座標をもとに圃場図をポリゴンSHPで作る。](https://github.com/mnltake/gpsnavi/blob/master/GPSのデータを使ってシェイプファイルの作成.md)  
↓  
2.圃場図を見ながら基準線ABを引きA(lat,lon),B(lat,lon)のポイント座標を得る  
↓  
3.A(lat,lon),B(lat,lon)をポリゴンの属性レコードに追加  
↓  
4.[現場でポリゴン属性を呼び出す。](https://github.com/mnltake/gpsnavi/blob/master/GPSの位置からシェイプファイルの属性データを取り出す.md)  
↓  
5.その時点のroverのh高さを与える（田面は水平と仮定）hは楕円体高　つまりbase Height + rover Up  
↓  
6.***A(lat,lon,h),B(lat,lon,h)をA(e,n,u),B(e,n,u)に変換***←ここ  
↓  
7.基準線ABが決まり即[基準線に平行な線をガイダンスできる](https://github.com/mnltake/gpsnavi/blob/master/Raspberry Piでcm精度のRTK-GPSガイダンスの制作(その２）.md)  
  
