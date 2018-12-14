#!/usr/bin/env python

import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BCM)

# GPIO2 : shutdown button
GPIO.setup(2, GPIO.IN)
# GPIO4 : reboot button
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def shutdown(channel):
  os.system("sudo shutdown -h now")

def reboot(channel):
  os.system("sudo reboot")

GPIO.add_event_detect(2, GPIO.FALLING, callback = shutdown, bouncetime = 2000)
GPIO.add_event_detect(4, GPIO.FALLING, callback = reboot, bouncetime = 2000)

while 1:
  time.sleep(100)
