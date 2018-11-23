#!/usr/bin/python
import time

from p_all import PROCESS_ALL

myApp = PROCESS_ALL()

def led_on():  print "led_on",
def led_off(): print "led_off"

myApp.led_on  = led_on
myApp.led_off = led_off

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

    myApp.run()
