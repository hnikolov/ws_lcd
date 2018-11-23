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

# TODO ------------------------------------------
PIN_LED = 26
GPIO.setup(PIN_LED, GPIO.OUT)

def led_on():  GPIO.output(PIN_LED, True)
def led_off(): GPIO.output(PIN_LED, False)

myApp.led_on  = led_on
myApp.led_off = led_off
# -----------------------------------------------

class LAST_TIME():
    W = 0.0
    G = 0.0
    E = 0.0

def cbk_w(channel):
    current_time = time.time() # sec.XX
    if current_time - LAST_TIME.W > 3.5: # sec
        myApp.w.add( 1 )

    LAST_TIME.W = current_time

def cbk_g(channel):
    current_time = time.time() # sec.XX
    if current_time - LAST_TIME.G > 3.5: # sec
        myApp.g.add( 0.01 )

    LAST_TIME.G = current_time
#        print "Gas IRQ took", round((time.time() - current_time)*1000, 3), "ms, pin =", GPIO.input(channel)

def cbk_e(channel):
    current_time = time.time() # sec.XX
    if current_time - LAST_TIME.E > 0.2: # sec
        myApp.e.add( 0.001 )

    LAST_TIME.E = current_time
# ============================================================================================
if __name__ == '__main__':

    GPIO.add_event_detect(PIN_WATER, GPIO.FALLING, callback = cbk_w, bouncetime = 300)
    GPIO.add_event_detect(PIN_GAS,   GPIO.FALLING, callback = cbk_g, bouncetime = 300)
    GPIO.add_event_detect(PIN_ELEC,  GPIO.FALLING, callback = cbk_e, bouncetime = 300)

    myApp.run()
