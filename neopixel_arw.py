#!/usr/bin/env python3
import time
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 13     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
levelcolor =[[255,0,0],[255,0,0],[255,0,0],[255,0,0],[255,0,0],[255,0,0],[10,10,10],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,0,255],[0,0,255]]
#赤　白　青
def colorarw(strip,arw):
    if arw > 12:
        arw = 12
    elif arw < -12:
        arw = -12
    aarw = int(arw/2 )
    n = aarw +6
    for i in range(13):
        strip.setPixelColorRGB(i,0,0,0)   
    strip.setPixelColorRGB(n, levelcolor[n][0],levelcolor[n][1],levelcolor[n][2]) 
    strip.setPixelColorRGB(6, levelcolor[6][0],levelcolor[6][1],levelcolor[6][2])
    strip.show()

if __name__ == '__main__':


    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    try:

        while True:
            for j in range(-13,13):
                colorarw(strip,j)
                time.sleep(0.05)
            for j in range(13,-13,-1):
                colorarw(strip,j)
                time.sleep(0.05)                
            
    except KeyboardInterrupt:
            colorarw(0)

