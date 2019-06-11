import pynmea2, serial
import pymap3d as pm
base = [34.9537979 ,136.9351043 ,87.02] #deg,deg,m

try:
    while True:

        try:
            # try to read a line of data from the serial port and parse
            with serial.Serial('COM11', 96000, timeout=1) as ser:
                # 'warm up' with reading some input
                #for i in range(10):
                 #   ser.readline()
                 # try to parse (will throw an exception if input is not valid NMEA)

                while True:
                    #print(ser)
                    msg = pynmea2.parse(ser.readline().decode('ascii', errors='replace'))
                    #print(msg)
                    if '$GPGGA' in str(msg):
                        #print(msg.latitude)
                        #print(msg.lat)
                        #print(msg.lon)
                        #print(msg.altitude)
                        rover =[msg.latitude ,msg.longitude ,msg.altitude] #deg,deg,m
                        rover_enu = pm.enu.geodetic2enu(rover[0] ,rover[1] ,rover[2],base[0] ,base[1] ,base[2])#m,m,m
                        print(rover_enu)

        except Exception as e:
            sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
        except KeyboardInterrupt as e:
            sys.stderr.write('Ctrl-C pressed, exiting log of %s to %s\n' % (port, outfname))

except KeyboardInterrupt:
    sys.stderr.write('Ctrl-C pressed, exiting port scanner\n')