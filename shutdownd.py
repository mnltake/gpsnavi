#!/usr/bin/env python
"""
Pin　7・5・11・GND
pin5をGNDにつなぐとRaspberryPiが起動する
http://www.aitendo.com/product/11784
shutdown-start-reboot
"""
import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BOARD)

# Pin7 : shutdown button
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# Pin11 : reboot button
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def shutdown(channel):
  os.system("sudo shutdown -h now")

def reboot(channel):
  os.system("sudo reboot")

GPIO.add_event_detect(7, GPIO.FALLING, callback = shutdown, bouncetime = 2000)
GPIO.add_event_detect(11, GPIO.FALLING, callback = reboot, bouncetime = 2000)

while 1:
  time.sleep(100)
