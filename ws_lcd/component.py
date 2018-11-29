# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

icons_list={u'chancerain':u'',u'chancesleet':u'','chancesnow':u'','chancetstorms':u'','clear':u'','flurries':u'','fog':u'','hazy':u'','mostlycloudy':u'','mostlysunny':u'','partlycloudy':u'','partlysunny':u'','sleet':u'','rain':u'','sunny':u'','tstorms':u'','cloudy':u''}
#flurries        u'\uf01b'
#mostlysunny     u'\uf00c'
#mostlycloudy    u'\uf031'
#partlycloudy    u'\uf002'
#partlysunny     u'\uf002'
#clear           u'\uf00d'
#sunny           u'\uf00d'
#cloudy          u'\uf031'
#hazy            u'\uf0b6'
#chancesnow      u'\uf00a'
#sleet           u'\uf0b2'
#tstorms         u'\uf033'
#fog             u'\uf014'
#rain            u'\uf008'
#chancesleet     u'\uf0b2'
#chancerain      u'\uf00d'
#chancetstorms   u'\uf01e'
# Cyrillic arial starts at 0x03
# supperscript of '3' u'\u00B3'
# subscript of '2' u'\u2083'

import os.path
path_prefix = os.path.dirname(__file__)
#print path_prefix 

# font_weather_icons = ImageFont.truetype(path_prefix + '/fonts/' + 'weathericons-regular-webfont.ttf', 35)
#draw.text((30,330),icons_list[str(icon)],font=font_weather_icons,fill=255)

# TODO: Magic constants
# TODO: Fonts and icons taken from local ws_epd folders. Allow for absolute paths as well
# TODO: Date and time as a separate component?

class Component(object):

    def __init__(self, width, height, bg_color = 255,          \
                       iw = 24,       ih = 24,  image = None,  \
                       font = 'arial.ttf', font_size = 14, format_string = "{}", align = 2):

        self.max_size = 128 # Screen size is 128 x 128 pixels
        
        self.set_color(bg_color)

        self.set_width(width)
        self.set_height(height)

        # position, to be set when building layout --------------------------------------
        self.x         = 0 #
        self.y         = 0 #
        self.rot       = 0 # Rotate the image when set in the frame memory (0, 90, 180, 270)
        # -------------------------------------------------------------------------------------

        # TODO rotate: self.lcd.set_frame_memory(c.image.transpose(Image.ROTATE_270), c.x, c.y)
        self.set_image(iw, ih, image)
        self.draw      = ImageDraw.Draw(self.image)
        self.font      = ImageFont.truetype(path_prefix + '/fonts/' + font, font_size)
#        self.font      = ImageFont.truetype(path_prefix + '/fonts/' + 'arial.ttf', font_size)
#        self.font      = ImageFont.truetype(path_prefix + '/fonts/' + 'weathericons-regular-webfont.ttf', font_size)
        self.aleft     = 0
        self.acenter   = 1
        self.aright    = 2
        self.align     = align

        self.invalid   = 1
        self.borders   = False # TODO
        
        self.value     = None
        self.fs        = format_string
        

    def set_color(self, bg_color):
#        self.bg        = 255 if bg_color == 255 else 0   # 0 - black, 255 - white
#        self.fg        = 0   if bg_color == 255 else 255
        self.bg        = (255,255,255) if bg_color == 255 else (0,0,0)
        self.fg        = (0,0,0) if bg_color == 255 else (255,255,255)
        
    def set_width(self, width):
        if width > self.max_size: print "Width is > 128. Set to 128"
        self.w = min(width, self.max_size)

    def set_height(self, height):
        if height > self.max_size: print "Height is > 128. Set to 128"
        self.h = min(height, self.max_size)

    # TODO: C:\Python27\lib\site-packages\PIL\Image.py:918: UserWarning: Palette images with Transparency   
    #       expressed in bytes should be converted to RGBA images
    # Get this if Image.new("RGB"...)
    def set_image(self, width, height, image):
        self.image = Image.new("RGB", (self.w, self.h), self.bg)
#        self.image = Image.new('1', (self.w, self.h), self.bg) # TODO 'RGB'
        if image != None:
            im = Image.open(path_prefix + '/icons/' + image)
            im = im.resize((width-2,height-2), Image.ANTIALIAS)
            # center image within component
            self.image.paste(im, ((self.w-width)/2, (self.h-height)/2+1))
#            self.image.paste(im, (1, 1)) # TODO

    def set_position(self, x, y, r=0):
        self.x   = x
        self.y   = y
        self.rot = r
        if self.w + self.x > self.max_size: print "X-position + height > 128"
        if self.h + self.y > self.max_size: print "Y-position + height > 128"


    def draw_borders(self):
        w = self.w if self.x + self.w < self.max_size else self.max_size - self.x
        self.draw.line((0,   0,        w-1, 0       ), fill=self.fg)
        self.draw.line((0,   0,        0,   self.h-1), fill=self.fg)
        self.draw.line((0,   self.h-1, w-1, self.h-1), fill=self.fg)
        self.draw.line((w-1, self.h-1, w-1, 0       ), fill=self.fg)
        self.invalid = 1


    def set_text(self, text, x=5, y=None, align=None):
        if align == None: align = self.align
        self.clear()
        if y == None: # Vertical center
            tx, ty = (0,0)
            w, h = self.draw.textsize(text, self.font)
            if align == self.aright:
                o = x if self.x + self.w < self.max_size else self.x + self.w - self.max_size + x
                tx = self.w - o - w
                ty = ((self.h - h) >> 1)-1
            elif align == self.aleft:
                tx = x
                ty = ((self.h - h) >> 1)-1
            elif align == self.acenter:
                tx = self.w/2-(w/2)
                ty = ((self.h - h) >> 1)-1

            self.draw.text((tx, ty), text, font = self.font, fill = self.fg)
#            self.draw.text((tx, ty),icons_list[u'chancerain'],font=self.font,fill=self.fg)

        else:
            self.draw.text((x, y), text, font = self.font, fill = self.fg)
        self.invalid = 1


    def clear(self):
        self.draw.rectangle((0, 0, self.w-1, self.h-1), fill=self.bg)
        self.invalid = 1

    def set(self,  value):
        if self.value != value:
            self.value = value
            self.set_text(self.fs.format(self.value))
        
    def add(self, value):
        self.value += value
        self.set_text(self.fs.format(self.value))
        
    def sub(self, value):
        self.value -= vlue
        self.set_text(self.fs.format(self.value))
        
    def get():
        return self.value
        
        
class Separator(Component):
    def __init__(self, width, height, bg_color = 255, x1=32, x2=48, image = None):
        super(Separator, self).__init__(width, height, font_size=3, bg_color=bg_color, image=image)
        self.draw.line((x1, height/2, x2, height/2), fill=self.fg)



# Currently, 24 bars graph in 120 pixels, 5 pixels per bar, including separation
# Component width can be 124 or 26
class BarGraph(Component):
    def __init__(self, width, height, bg_color = 255, image = None):
        self.small = 26
        w = self.small if width < 64 else 124
        super(BarGraph, self).__init__(w, height, font_size=3, bg_color=bg_color, image=image)
        
        self.nbars   = 24
        self.bars    = [0] * self.nbars
        self.max     = 0
        self.scale_f = 1.0
        self.draw_lines()
    
    def draw_lines(self):
        self.draw.line((2, self.h/2, self.w-2, self.h/2), fill=self.fg) # Middle
#        self.draw.line((2, self.h-1, self.w-2, self.h-1), fill=self.fg) # Bottom

        # For width=124 and 26, bar width=3 and 1, vertical lines at 6, 12, 18 o'clock
        #pos = self.w/4 if self.w == self.small else self.w/4 - 1 # ((self.w/4 % 2) == 0)
        #y = 2 if self.w == self.small else self.h
        if self.w == self.small:
            #pos = self.w/4 
            #y = 2
            #self.draw.line((  pos, 0,   pos, y), fill=self.fg) # Vertical
            #self.draw.line((2*pos, 0, 2*pos, y), fill=self.fg) # Vertical
            #self.draw.line((3*pos, 0, 3*pos, y), fill=self.fg) # Vertical
            pass
        else:
            pos = self.w/4 - 1
            y = self.h
            self.draw.line((  pos-1, 0,   pos-1, y), fill=self.fg) # Vertical
            self.draw.line((2*pos-1, 0, 2*pos-1, y), fill=self.fg) # Vertical
            self.draw.line((3*pos-1, 0, 3*pos-1, y), fill=self.fg) # Vertical
        
    def clear_bars(self):
        self.bars    = [0] * self.nbars
        self.max     = 0
        self.scale_f = 1.0
        self.invalid = 1
        
    def set_bar(self, position, value):
        if position > self.nbars-1:
            print "Wrong position:", position, "Set to 0"
            position = 0
            
        self.bars[position] = value
        if value > self.max:
            self.max = value
            y = 4 if self.w == self.small else 2
            self.scale_f = (self.h-y)/float(self.max)
            
        self.update()
        
    def update(self):        
        self.clear()
        self.draw_lines()
        for i, h in enumerate(self.bars):
            sh = self.scale_f * h
            if self.w == self.small:
                if sh < 2: sh = 2
                # for width=26, bar width=1
                offset = 1 + i
                self.draw.line((offset, self.h-sh, offset, self.h-2), fill=self.fg)
            else:
                # for width=124, bar width=3
                offset = 3 + (5 * i)
                self.draw.rectangle((offset, self.h-sh, offset+2, self.h), fill=self.fg)
               
# TODO: line graph
        # for i in range(1,len(self.bars)):
            # sh  = self.scale_f * self.bars[i-1]
            # sh1 = self.scale_f * self.bars[i]
            # offset = 4 + (5 * i)
            # self.draw.line((offset, self.h-sh, offset+5, self.h-sh1), fill=self.fg)
            # # for width=26
# #            offset = 1 + i
# #            self.draw.line((offset, self.h-sh, offset+1, self.h-sh1), fill=self.fg)
        self.invalid = 1