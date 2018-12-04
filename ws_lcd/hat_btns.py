#!/usr/bin/python
from lcd_logger import MQTT_LOGGER

myApp = MQTT_LOGGER(WS=True)

class G():
    BACKLIGHT = True

import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

# BCM
#KEY_1  = 21
#KEY_2  = 20
#KEY_3  = 16
#JSK_UP = 6
#JSK_DN = 19
#JSK_LT = 5
#JSK_RT = 26
#JSK_PS = 13
#BL     = 24

# Board
KEY_1  = 40
KEY_2  = 38
KEY_3  = 36
JSK_UP = 31
JSK_DN = 35
JSK_LT = 29
JSK_RT = 37
JSK_PS = 33
BL     = 18

GPIO.setup(KEY_1,  GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(KEY_2,  GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(KEY_3,  GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(JSK_UP, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(JSK_DN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(JSK_LT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(JSK_RT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(JSK_PS, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BL, GPIO.OUT)

def cbk_key_1 (channel):
    myApp.display_next()

def cbk_key_2 (channel):
    myApp.display_prev()

def cbk_key_3 (channel):
    backlight_toggle()

def cbk_jsk_up(channel):
    myApp.display_next()

def cbk_jsk_dn(channel):
    myApp.display_prev()

def cbk_jsk_lt(channel):
    myApp.display_hour_prev()

def cbk_jsk_rt(channel):
    myApp.display_hour_next()

def cbk_jsk_ps(channel):
    backlight_toggle()

# ------------------------------------
def backlight_off():
    G.BACKLIGHT = False
    GPIO.output(BL, G.BACKLIGHT)

def backlight_toggle():
    G.BACKLIGHT = not G.BACKLIGHT
    GPIO.output(BL, G.BACKLIGHT)


# ============================================================================================
if __name__ == '__main__':

    GPIO.add_event_detect(KEY_1,  GPIO.FALLING, callback = cbk_key_1,  bouncetime = 300)
    GPIO.add_event_detect(KEY_2,  GPIO.FALLING, callback = cbk_key_2,  bouncetime = 300)
    GPIO.add_event_detect(KEY_3,  GPIO.FALLING, callback = cbk_key_3,  bouncetime = 300)
    GPIO.add_event_detect(JSK_UP, GPIO.FALLING, callback = cbk_jsk_up, bouncetime = 300)
    GPIO.add_event_detect(JSK_DN, GPIO.FALLING, callback = cbk_jsk_dn, bouncetime = 300)
    GPIO.add_event_detect(JSK_LT, GPIO.FALLING, callback = cbk_jsk_lt, bouncetime = 300)
    GPIO.add_event_detect(JSK_RT, GPIO.FALLING, callback = cbk_jsk_rt, bouncetime = 300)
    GPIO.add_event_detect(JSK_PS, GPIO.FALLING, callback = cbk_jsk_ps, bouncetime = 300)

#    backlight_off()
    myApp.run()
