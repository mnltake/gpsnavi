#RELPOSNED and PVT

def readUBX(readbytes):
    RELPOSNED = b'\x3c'
    PVT =b'\x07'
    POSLLH = b'\x02'
    msg = dict()
    j=0   
    while j < len(readbytes) : 
        i = 0
        payloadlength = 0
        ackPacket=[b'\xB5',b'\x62',b'\x01',b'\x00',b'\x00',b'\x00']
        while i < payloadlength +8:              
            if j < len(readbytes) :
                incoming_byte = readbytes[j]   
                j += 1
            else :
                break
            if (i < 3) and (incoming_byte == ackPacket[i]):
                i += 1
            elif i == 3:
                ackPacket[i]=incoming_byte
                i += 1              
            elif i == 4 :
                ackPacket[i]=incoming_byte
                i += 1
            elif i == 5 :
                ackPacket[i]=incoming_byte        
                payloadlength = int.from_bytes(ackPacket[4]+ackPacket[5], byteorder='little',signed=False) 
                i += 1
            elif (i > 5) :
                ackPacket.append(incoming_byte)
                i += 1
        if checksum(ackPacket,payloadlength) :
            if ackPacket[3] == RELPOSNED:
                msg.update(perseNED(ackPacket))
            elif ackPacket[3] == POSLLH:
                msg.update(perseLLH(ackPacket))
            elif ackPacket[3] == PVT:
                msg.update(persePVT(ackPacket))
    return msg

def checksum(ackPacket,payloadlength ):
    CK_A =0
    CK_B =0
    for i in range(2, payloadlength+ 6):
        CK_A = CK_A + int.from_bytes(ackPacket[i], byteorder='little',signed=False) 
        CK_B = CK_B +CK_A
    CK_A &=0xff
    CK_B &=0xff
    if (CK_A ==  int.from_bytes(ackPacket[-2], byteorder='little',signed=False)) and (CK_B ==  int.from_bytes(ackPacket[-1], byteorder='little',signed=False)):
        #print("ACK Received")
        return True
    else :
        print("ACK Checksum Failure:")  
        return False

def perseNED(ackPacket):
    posned = dict()
    #relPosN
    byteoffset =8 + 6
    bytevalue =  ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posned["N"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    posned["NH"] = int.from_bytes(ackPacket[32 + 6], byteorder='little',signed=True) 

    #relPosE
    byteoffset =12 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posned["E"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    posned["EH"] = int.from_bytes(ackPacket[33 + 6], byteorder='little',signed=True) 

    #relPosD
    byteoffset =16 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posned["D"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    posned["DH"] = int.from_bytes(ackPacket[33 + 6], byteorder='little',signed=True)     #print("D:%0.2f cm" %posned["D"]  )

    #Carrier solution status
    flags = int.from_bytes(ackPacket[60 + 6], byteorder='little',signed=True) 
    posned["gnssFixOk"] =  flags  & (1 << 0) #gnssFixOK 
    posned["carrSoln"] =  (flags   & (0b11 <<3)) >> 3 #carrSoln0:no carrier 1:float 2:fix

    #GPS time
    byteoffset =4 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posned["iTow"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #relPosLength
    byteoffset =20 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posned["length"] = int.from_bytes(bytevalue, byteorder='little',signed=False) 
    posned["lengthH"] = int.from_bytes(ackPacket[35 + 6], byteorder='little',signed=True) 

    #relPosHeading
    byteoffset =24 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posned["heading"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
    
    return posned

def perseLLH(ackPacket):
    posllh=dict()
    #PosLon
    byteoffset = 4 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posllh["Lon"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #PosLat
    byteoffset =8 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posllh["Lat"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #posHeight
    byteoffset =12 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posllh["Height"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #Height above mean sea level
    byteoffset =16 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    posllh["hMSL"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    return posllh

def persePVT(ackPacket):
    pospvt=dict()
    #Year
    byteoffset = 4 + 6
    bytevalue = ackPacket[byteoffset] 
    bytevalue  +=  ackPacket[byteoffset+1] 
    pospvt["year"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #month day hour min sec
    byteoffset =6 + 6
    b=0
    for key in ("month", "day", "hour", "min", "sec"):
        bytevalue  =  ackPacket[byteoffset+b] 
        pospvt[key] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
        b +=1

    #PosLon
    byteoffset = 24 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    pospvt["Lon"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 
  
    #PosLat
    byteoffset =28 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    pospvt["Lat"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #posHeight
    byteoffset =32 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    pospvt["Height"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #Height above mean sea level
    byteoffset =36 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    pospvt["hMSL"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #Ground Speed
    byteoffset =60 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    pospvt["gSpeed"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    #Heading of motion
    byteoffset =64 + 6
    bytevalue = ackPacket[byteoffset] 
    for i in range(1,4):
        bytevalue  +=  ackPacket[byteoffset+i] 
    pospvt["headMot"] = int.from_bytes(bytevalue, byteorder='little',signed=True) 

    return pospvt

def llh2enu(msg):
    basellh = (34.95379794,136.9351043,87.02)#RTK_BASE lat(deg) lon(deg) heigh(m)
    rover =(msg["Lat"]*0.0000001 ,msg["Lon"]*0.0000001 ,msg["Height"]*0.001) #deg,deg,m
    rover_enu = geodetic2enu(rover[0] ,rover[1] ,rover[2],basellh[0] ,basellh[1] ,basellh[2] )
    msg["e"]=rover_enu[0]*100 #cm
    msg["n"]=rover_enu[1]*100
    msg["u"]=rover_enu[2]*100

if __name__ == "__main__":
    import serial
    import pprint
    from pymap3d.enu import  geodetic2enu
    lenRELPOSNED = 6 + 64 +2
    lenPOSLLH = 6 + 28 + 2
    lenPVT = 6 + 92 +2
    buffsize = lenRELPOSNED + lenPVT #172
    #buffsize = lenRELPOSNED + lenPOSLLH #108
    #buffsize = lenRELPOSNED #72
    while 1:
        with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
            readbytes =[] 
            for i in range(buffsize):
                readbytes.append(ser.read())
        ubxmsg=readUBX(readbytes)
        llh2enu(ubxmsg)
        pprint.pprint(ubxmsg)
"""
ubxmsg['*']     ex. northcm =ubxmsg['N']
    (RELPOSNED)
        N   cm
        E   cm
        D   cm
        NH  0.1mm
        EH  0.1mm
        DH  0.1mm
        lengh   cm
        lengthH 0.1mm
        heading 0.00001deg(1e-5)
        carrSoln    0:no carrier 1:float 2:fix
        gnssFixOk   0:no 1:ok
        iTow    ms GPS time of week
    (PVT)
        year    UTC
        month
        day
        hour
        min
        sec
        Lon  0.0000001deg(1e-7)
        Lat  0.0000001deg(1e-7)
        Height  mm  Heigth above ellpsoid
        hMSL    mm  Height above mean sea level
        gSpeed  mm/s    Ground speed
        headMot 0.00001deg(1e-5) Heading of motion
"""




