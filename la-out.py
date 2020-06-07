#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(10, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

print("run actuator direction 1 for 5 seconds")
#GPIO.output(10,GPIO.LOW)
GPIO.output(25, GPIO.HIGH)
time.sleep(5)
print("stop 5 seconds")
#time.sleep(5)
#GPIO.output(10, GPIO.LOW)
#GPIO.output(25, GPIO.LOW)
print ("run actuator direction 2 for 5 seconds")
#GPIO.output(10, GPIO.LOW)
#GPIO.output(25, GPIO.HIGH)
#time.sleep(5)
print("stop actuator program end") 
        
