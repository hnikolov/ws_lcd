#!/usr/bin/python
import paho.mqtt.client as mqtt
import datetime, sys
import time

from process_all import PROCESS_ALL

myApp = PROCESS_ALL()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

PIN_WATER = 19
PIN_GAS   = 20
PIN_ELEC  = 16

GPIO.setup(PIN_WATER, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(PIN_GAS,   GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(PIN_ELEC,  GPIO.IN, pull_up_down = GPIO.PUD_UP)

class LAST_TIME():
    W = 0.0
    G = 0.0
    E = 0.0
        
def cbk_w(channel):
    current_time = time.time() # sec.XX
    if current_time - LAST_TIME.W > 3.5: # sec
        myApp.w += 1

    LAST_TIME.W = current_time

def cbk_g(channel):
    current_time = time.time() # sec.XX
    if current_time - LAST_TIME.G > 3.5: # sec
        myApp.g += 0.01
        
    LAST_TIME.G = current_time
#        print "Gas IRQ took", round((time.time() - current_time)*1000, 3), "ms, pin =", GPIO.input(channel)

def cbk_e(channel):
    current_time = time.time() # sec.XX
    if current_time - LAST_TIME.E > 0.2: # sec
        myApp.e += 0.001
        
    LAST_TIME.E = current_time
# ============================================================================================
if __name__ == '__main__':

    myApp = MQTT_Connection()

    GPIO.add_event_detect(PIN_WATER, GPIO.FALLING, callback = myApp.cbk_w, bouncetime = 300)
    GPIO.add_event_detect(PIN_GAS,   GPIO.FALLING, callback = myApp.cbk_g, bouncetime = 300)
    GPIO.add_event_detect(PIN_ELEC,  GPIO.FALLING, callback = myApp.cbk_e, bouncetime = 300)

    myApp.run()
