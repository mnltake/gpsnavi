前回の記事(https://github.com/mnltake/gpsnavi/blob/master/続・Raspberry Piでcm精度のRTK-GPSガイダンスの制作（2周波へ向けて）.md)  
では　u-blox ZED-F9P(以下F9P)内部でRTK演算を行い、NMEAから立体座標へはラズパイ内でしていましたが回りくどいやり方が気になってました。  
そこでF9P内部で立体座標まで変換し出力されたバイナリデータをpythonを使って解読できたのでその紹介です  
# 参考資料  
まずF9Pのプロトコル資料を読みます  
https://www.u-blox.com/sites/default/files/u-blox_ZED-F9P_InterfaceDescription_%28UBX-18010854%29.pdf  
（こちらはM8Pの資料）  
https://www.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_(UBX-13003221)_Public.pdf  
  
バイナリデータの解読方法についてはこちらを参考にしました（arduino用）  
https://github.com/aortner/f9dualheadingarduinomega  
  
関係するところはこのあたり  
(page29)  
>5.2 UBX Frame Structure  
  
(page31)  
>5.4 UBX Checksum  
  
(page158)  
>5.14.12 UBX-NAV-RELPOSNED (0x01 0x3C)  
  
baseを原点としたN（北）E（東）D（下）の座標とベクトル（距離、方位）が出力されます  
  
Little-Endian　とか　Checksum　とか説明してあるのでググってください  
  
  
u-centerの設定でF9Pの出力を  
MSG-**(01-3C)NAV-RELPOSNED** をUSBから出力  
RTCMは前回と同じくstr2strを使いF9P-UART2から入力  
  
# Pythonで解読  
```readNED.py
import serial

nowPoint=[0]*8
HEADER = 6

def readPosned():
    ackPacket=[b'\xB5',b'\x62',b'\x01',b'\x3C',b'\x00',b'\x00']
    i = 0
    payloadlength = 6
    with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
        while i < payloadlength+8: 
            incoming_char = ser.read()            
            if (i < 3) and (incoming_char == ackPacket[i]):
                i += 1
            elif i == 3:
                ackPacket[i]=incoming_char
                i += 1              
            elif i == 4 :
                ackPacket[i]=incoming_char
                i += 1
            elif i == 5 :
                ackPacket[i]=incoming_char        
                payloadlength = int.from_bytes(ackPacket[4]+ackPacket[5], byteorder='little',signed=False) 
                i += 1
            elif (i > 5):
                ackPacket.append(incoming_char)
                i += 1

    if checksum(ackPacket,payloadlength) :
        perseNED(ackPacket)


def checksum(ackPacket,payloadlength ):
    CK_A =0
    CK_B =0
    for i in range(2, payloadlength+6):
        CK_A = CK_A + int.from_bytes(ackPacket[i], byteorder='little',signed=False) 
        CK_B = CK_B +CK_A
        #print(j)
    CK_A &=0xff
    CK_B &=0xff
    if (CK_A ==  int.from_bytes(ackPacket[-2], byteorder='little',signed=False)) and (CK_B ==  int.from_bytes(ackPacket[-1], byteorder='little',signed=False)):
        #print("ACK Received")
        return True
    else :
        print("ACK Checksum Failure:")  
        return False

def perseNED(ackPacket):
    #relPosN
    byteoffset =8 +HEADER
    bytevalue =  ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    nowPoint[0] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    nowPoint[0] += (int.from_bytes(ackPacket[32 + HEADER], byteorder='little',signed=True) )/100
    print("N:%0.2f cm" %nowPoint[0]  )
    #relPosE
    byteoffset =12 +HEADER
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    nowPoint[1] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    nowPoint[1] += (int.from_bytes(ackPacket[33 + HEADER], byteorder='little',signed=True) )/100
    print("E:%0.2f cm" %nowPoint[1]  )
    #relPosD
    byteoffset =16 +HEADER
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    nowPoint[2] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    nowPoint[2] += (int.from_bytes(ackPacket[33 + HEADER], byteorder='little',signed=True) )/100
    print("D:%0.2f cm" %nowPoint[2]  )
    #Carrier solution status
    flags = int.from_bytes(ackPacket[60 + HEADER], byteorder='little',signed=True) 
    nowPoint[3] =  flags  & (1 << 0) #gnssFixOK 
    nowPoint[4] =  (flags   & (0b11 <<3)) >> 3 #carrSoln0:no carrier 1:float 2:fix
    print("gnssFixOk:%d" %nowPoint[3])
    print("carrSoln:%d" %nowPoint[4])
    #GPS time
    byteoffset =4 +HEADER
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    nowPoint[5] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    print("iTow:%0.1f" %float(nowPoint[5]/1000))
    #relPosLength
    byteoffset =20 +HEADER
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    nowPoint[6] = int.from_bytes(bytevalue, byteorder='little',signed=False) 
    nowPoint[6] += (int.from_bytes(ackPacket[35 + HEADER], byteorder='little',signed=True) ) /100
    print("length:%0.1f cm" %float(nowPoint[6]))
    #relPosHeading
    byteoffset =24 +HEADER
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    nowPoint[7] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    print("heading:%f deg" %float(nowPoint[7]/100000))

    return nowPoint
while 1:
    readPosned()
```  
  
N:-187.40 cm  
E:432.11 cm  
D:405.27 cm  
gnssFixOk:1  
carrSoln:1  
iTow:302468.0  
length:621.4 cm  
heading:113.445720   
こんな感じで出ました  
  
# 応用できること  
ラズパイZEROやESP32などのマイコンでも簡単な計算で座標が使える（別途RTCM補正信号の入力は必要）  
ので、サイクルコンピューターのような走行距離の計算や、面積計算、高度差測定などがcm精度で行える  
２台使って（moving base）ジャイロセンサーのようにRoll,Yaw,Pitchが求められる  
  
# Github  
https://github.com/mnltake/readF9P_UBX  
で更新中  
