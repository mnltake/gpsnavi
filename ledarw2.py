#! /user/bin/env python

import RPi.GPIO as GPIO
import time
#GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
pins =  [40, 38, 36, 32, 26, 24, 22, 18, 16, 12, 10, 8]

GPIO.setup( pins , GPIO.OUT )
GPIO.output( pins , GPIO.LOW )


def ledarw( arw ,ledpins):
    pins = ledpins
    r = pins[10]
    l = pins[11]
    GPIO.output(pins , GPIO.LOW )
    if -2<= arw <= 2:
        GPIO.output(pins[:9] , GPIO.LOW )
        GPIO.output(pins[10:] , GPIO.HIGH )
    elif arw  < -2 :
        GPIO.output( r , GPIO.HIGH ) # 右
        GPIO.output( l , GPIO.LOW) 
    elif arw > 2  :
        GPIO.output( l , GPIO.HIGH ) #　左
        GPIO.output( r , GPIO.LOW) 
    if arw >= 22 :
        arw = 22
    elif arw <= -22 :
        arw = -22
    aarw = abs(arw) / 2 - 1    
    i = 0
    while i < aarw :
        GPIO.output( pins[i], GPIO.HIGH )
        i= i+1

def ledbar( arw ,ledpins):
    pins = ledpins
    r = pins[10]
    l = pins[11]
    GPIO.output(pins , GPIO.LOW )
    if -2<= arw <= 2:
        GPIO.output(pins[:9] , GPIO.LOW )
        GPIO.output(pins[10:] , GPIO.HIGH )
    elif arw  < -2 :
        GPIO.output( r , GPIO.HIGH ) # 右
        GPIO.output( l , GPIO.LOW) 
    elif arw > 2  :
        GPIO.output( l , GPIO.HIGH ) #　左
        GPIO.output( r , GPIO.LOW) 
    if arw >= 22 :
        arw = 22
    elif arw <= -22 :
        arw = -22
    aarw = abs(arw) / 2 - 1    
    i = 0
   
    GPIO.output( pins[aarw], GPIO.HIGH )
         
GPIO.cleanup()           
if __name__ == '__main__':
    while true:
        for i range(-22,22):
            ledarw( i ,ledpins)

        for j range(-22,22):
            ledbar( j ,ledpins)