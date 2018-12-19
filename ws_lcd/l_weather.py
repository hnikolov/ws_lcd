# -*- coding: utf-8 -*-
import time
from layout import Layout
from component import *

class Layout_EUR(Layout):
    def __init__(self):
        super(Layout_EUR, self).__init__(color = "black")

        self.ch1     = 18 # component height 1
        self.ch2     = 20 # component height 2
        self.sh1     =  2 # separator height 1

        # Offsets
        self.row_1_y = self.ch2
        self.sep_2_y = self.row_1_y + 2*self.ch2
        self.row_2_y = self.sep_2_y + self.sh1
        self.sep_3_y = self.row_2_y + self.ch2
        self.row_3_y = self.sep_3_y + self.sh1
        self.sep_4_y = self.row_3_y + self.ch2
        self.row_4_y = self.sep_4_y + self.sh1

        
        # Build the layout
        self.mi   = Component(self.ch2, self.ch2, font='weathericons-regular-webfont.ttf', font_size=14, bg_color=0, align=1)
        self.mi.set_position(2, 0)
        self.mi.set_text(u'\uF0E2', y=-1) # Moon phase
        
        self.cdate = Component(52, self.ch2, font_size=14, bg_color=0, align=1)
        self.cdate.set_position(20, 0)
        self.cdate.set(time.strftime('%d-%b'))

        self.ctime = Component(56, self.ch2, font_size=14, bg_color=0, align=1)
        self.ctime.set_position(72, 0)
        self.ctime.set(time.strftime('%H:%M'))
        # ----------------
        self.ewi   = Component(48, 2*self.ch2, font_size=24, align=1)
        self.ewi.set_position(0, self.row_1_y)
        self.ewi.set_text("-23" + u'\N{DEGREE SIGN}')

        self.ewu   = Component(48, 2*self.ch2, font='weathericons-regular-webfont.ttf', font_size=26, bg_color=255, align=1)
        self.ewu.set_position(44, self.row_1_y)
        self.ewu.set_text(u'\uF002') # Weather icon

        self.ewi0   = Component(34, self.ch2, font_size=14, align=0)
        self.ewi0.set_position(94, self.row_1_y)
        self.ewi0.set_text("-18" + u'\N{DEGREE SIGN}')
        
        self.ewi1   = Component(34, self.ch2, font_size=14, align=0)
        self.ewi1.set_position(94, self.row_1_y + self.ch2)
        self.ewi1.set_text("-27" + u'\N{DEGREE SIGN}')
        # -----------------------------        
        self.eti   = Component(92, self.ch2, font_size=13, font='Roboto-Condensed.ttf', align=1)
        self.eti.set_position(0, self.row_2_y)
        self.eti.set_text("Valkenburg, ZH")

        self.eti0   = Component(34, self.ch2, font_size=22, font='weathericons-regular-webfont.ttf', align=1)
        self.eti0.set_position(94, self.row_2_y)
        self.eti0.set_text(u'\uF058') # Arrow up: f058, down: f044

        # -------------------------------------        
#        self.egi   = Component(self.ch2, self.ch2, font='weathericons-regular-webfont.ttf', font_size=20, bg_color=0)
        self.egi   = Component(self.ch2, self.ch2, font='weathericons-regular-webfont.ttf', font_size=16, bg_color=0)
        self.egi.set_position(0, self.row_3_y)
#        self.egi.set_text(u'\uF078', align=1) # Humidity: F07A
        self.egi.set_text(u'\uF07A', align=1) # Humidity

        self.egv   = Component(44, self.ch2, font_size=18, font='Roboto-Condensed.ttf', format_string = "{}%", align=0, bg_color=0)
        self.egv.set_position(20, self.row_3_y)
        self.egv.set(67)

        self.eri   = Component(24, self.ch2, font='weathericons-regular-webfont.ttf', font_size=16, bg_color=0)
        self.eri.set_position(66, self.row_3_y)
        self.eri.set_text(u'\uF084', align=1) # Umbrella

        self.egu   = Component(38, self.ch2, font_size=18, font='Roboto-Condensed.ttf', bg_color=0)
        self.egu.set_position(90, self.row_3_y)
        self.egu.set_text("26%", align=0)
        
        self.eei   = Component(self.ch2, self.ch2, font_size=18, font='weathericons-regular-webfont.ttf', bg_color=0)
        self.eei.set_position(0, self.row_4_y)
        self.eei.set_text(u'\uF079', x=0, align=1) # Barometer

        self.eev   = Component(64, self.ch2, font_size=18, format_string="{0:.1f}", align=0, bg_color=0)
        self.eev.set_position(20, self.row_4_y)
        self.eev.set(1023.52)

        self.eev0   = Component(34, self.ch2, font='weathericons-regular-webfont.ttf', font_size=20, bg_color=0, align=0)
        self.eev0.set_position(94, self.row_4_y)
        self.eev0.set_text(u'\uF0B7') # Wind
        
#        self.eeu   = Component(32, self.ch2, font_size=16)
#        self.eeu.set_position(92, self.row_3_y)
#        self.eeu.set_text(u'\u20AC', x=0, align=0) # Euro

#        self.eti   = Component(128, 14, font_size=11, font='Roboto-Condensed.ttf', align=1)
#        self.eti.set_position(0, self.row_4_y+8)
#        self.eti.set_text("Overcast throughout the day.")

#        self.etv   = Component(64, self.ch2, font_size=18, format_string="{0:.2f}")
#        self.etv.set_position(28, self.row_4_y)

#        self.etu   = Component(32, self.ch2, font_size=16)
#        self.etu.set_position(92, self.row_4_y)
#        self.etu.set_text(u'\u20AC', x=0, align=0) # Euro

        # Add components to the layout
        self.add([self.mi, self.cdate, self.ctime])
#        self.add([self.ewi, self.ewv, self.ewu])
        self.add([self.ewi,            self.ewu, self.ewi0, self.ewi1])
#        self.add([self.egv, self.egu])
        self.add([self.egi, self.egv, self.eri, self.egu])
        self.add([self.eei, self.eev, self.eev0])
#        self.add([self.eei, self.eev, self.eeu])
        self.add([self.eti, self.eti0])
#        self.add([self.eti, self.etv, self.etu])

        self.clear_all()

    def clear_all(self):
        pass
#        self.ewv.set(0.0)
#        self.egv.set(0.0)
#        self.eev.set(0.0)
#        self.etv.set(0.0)


    def set_date_time(self):
#        tdate = time.strftime('%d-%b-%y')
        self.cdate.set(time.strftime('%d-%b'))
        self.ctime.set(time.strftime('%H:%M'))
        
    def update_total(self):
        pass
        #self.etv.set(self.eev.value)

if __name__ == '__main__':

    from lcd import LCD

    # Display Layout instance
    L2 = Layout_EUR()

    # LCD instance
    lcd = LCD(False)       
    lcd.draw(L2)
        
    raw_input()
    lcd.close()
