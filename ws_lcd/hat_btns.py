#!/usr/bin/python
""" Testing the 3 keys and the 5-key joystick of Waveshare 1in44-LCD-HAT """
import st7735s as controller
import time
from PIL import Image

screen = controller.ST7735S()

img1 = Image.open("assets/1.jpg")
img2 = Image.open("assets/2.png")
img3 = Image.open("assets/sky.bmp")
img4 = Image.open("assets/time.bmp")

class G():
    L_IMG     = [img1, img2, img3, img4]
    L_SIZE    = len(L_IMG)
    L_IDX     = 0
    BACKLIGHT = False

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
#    print "Key 1"
    img_next()

def cbk_key_2 (channel):
#    print "Key 2"
    img_prev()

def cbk_key_3 (channel):
#    print "Key 3"
    backlight_toggle()

def cbk_jsk_up(channel):
#    print "Joystick Up"
    img_next()

def cbk_jsk_dn(channel):
#    print "Joystick Down"
    img_prev()

def cbk_jsk_lt(channel):
#    print "Joystick Left"
    img_prev()

def cbk_jsk_rt(channel):
#    print "Joystick Right"
    img_next()

def cbk_jsk_ps(channel):
#    print "Joystick Press"
    backlight_toggle()

# ------------------------------------
def backlight_off():
    G.BACKLIGHT = False
    GPIO.output(BL, G.BACKLIGHT)

def backlight_toggle():
    G.BACKLIGHT = not G.BACKLIGHT
    GPIO.output(BL, G.BACKLIGHT)

def img_next():
    G.L_IDX = (G.L_IDX + 1) % G.L_SIZE
    screen.draw( G.L_IMG[G.L_IDX] )

def img_prev():
    G.L_IDX = (G.L_IDX - 1) % G.L_SIZE
    screen.draw( G.L_IMG[G.L_IDX] )

def run():
    try:
        backlight_off()
        screen.draw( G.L_IMG[G.L_IDX] )
        while True: time.sleep(10)

    except (KeyboardInterrupt, SystemExit, Exception) as e:
        print "Exit...", e
        screen.close()
        GPIO.cleanup()

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

    run()
