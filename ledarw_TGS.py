#! /user/bin/env python3
def ledarw( arw ,ledpins):
    import RPi.GPIO as GPIO
    pins = ledpins
    r = pins[8]
    l = pins[7]
    GPIO.output(pins , GPIO.HIGH)
    if -2<= arw <= 2:
        GPIO.output(pins[:6] , GPIO.HIGH )
        GPIO.output(pins[7:] , GPIO.LOW )
    elif arw  < -2 :
        GPIO.output( r , GPIO.HIGH ) # 右
        GPIO.output( l , GPIO.LOW) 
    elif arw > 2  :
        GPIO.output( l , GPIO.HIGH ) #　左
        GPIO.output( r , GPIO.LOW) 
    if arw >= 14 :
        arw = 14
    elif arw <= -14 :
        arw = -14
    aarw = abs(arw) / 2 - 1    
    i = 0
    while i < aarw :
        GPIO.output( pins[i], GPIO.LOW )
        i= i+1

def ledbar( arw ,ledpins):
    import RPi.GPIO as GPIO
    pins = ledpins
    r = pins[8]
    l = pins[7]
    GPIO.output(pins[:7] , GPIO.HIGH )
    if -2<= arw <= 2:
        GPIO.output(pins[7:] , GPIO.LOW )
    elif arw  < -2 :
        GPIO.output( r , GPIO.HIGH ) # 右
        GPIO.output( l , GPIO.LOW) 
    elif arw > 2  :
        GPIO.output( l , GPIO.HIGH ) #　左
        GPIO.output( r , GPIO.LOW) 
    if arw >= 14 :
        arw = 14
    elif arw <= -14 :
        arw = -14
    aarw = abs(arw) / 2  -1

    if aarw >= 0:
        i = int(aarw)
        GPIO.output( pins[i], GPIO.LOW )
         
    
if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BOARD)
   # ledpins =  [36,24,22,40,18,16,38,26,32]
    ledpins =  (38,16,18,40,22,24,36,26,32)
    GPIO.cleanup()
    GPIO.setup( ledpins , GPIO.OUT )
    GPIO.output( ledpins , GPIO.HIGH )
    while 1:
        for i in range(-14,15):
            print(i)
            ledbar( i ,ledpins)
            time.sleep(0.5)
      
        for j in range(-20,20):
            ledbar( j ,ledpins)
            time.sleep(0.2)
