# -*- coding: utf-8 -*-
import time
from layout import Layout
from component import *

class Layout_EUR(Layout):
    def __init__(self):
        super(Layout_EUR, self).__init__(color = "black")

        self.ch1     = 18 # component height 1
        self.ch2     = 25 # component height 2
        self.sh1     =  2 # separator height 1

        # Offsets
        self.row_1_y = self.ch1
        self.sep_2_y = self.row_1_y + self.ch2
        self.row_2_y = self.sep_2_y + self.sh1
        self.sep_3_y = self.row_2_y + self.ch2
        self.row_3_y = self.sep_3_y + self.sh1
        self.sep_4_y = self.row_3_y + self.ch2
        self.row_4_y = self.sep_4_y + self.sh1

        # Build the layout
        self.cdate = Component(72, self.ch1, font_size=14, bg_color=0, align=1)
        self.cdate.set_position(0, 0)
        self.cdate.set(time.strftime('%d-%b'))

        self.ctime = Component(56, self.ch1, font_size=14, bg_color=0, align=1)
        self.ctime.set_position(72, 0)
        self.ctime.set(time.strftime('%H:%M'))
        # ----------------
        self.ewi   = Component(self.ch2, self.ch2, font_size=20, image='tap-water1.jpg')
        self.ewi.set_position(4, self.row_1_y)

        self.ewv   = Component(64, self.ch2, font_size=18, format_string="{0:.2f}")
        self.ewv.set_position(28, self.row_1_y)

        self.ewu   = Component(32, self.ch2, font_size=16)
        self.ewu.set_position(92, self.row_1_y)
        self.ewu.set_text(u'\u20AC', x=0, align=0) # Euro

        self.egi   = Component(self.ch2, self.ch2, font_size=20, image='gas_32x32.png')
        self.egi.set_position(4, self.row_2_y)

        self.egv   = Component(64, self.ch2, font_size=18, format_string="{0:.2f}")
        self.egv.set_position(28, self.row_2_y)

        self.egu   = Component(32, self.ch2, font_size=16)
        self.egu.set_position(92, self.row_2_y)
        self.egu.set_text(u'\u20AC', x=0, align=0) # Euro
        
        self.eei   = Component(self.ch2, self.ch2, font_size=20, image='plug1.png')
        self.eei.set_position(4, self.row_3_y)

        self.eev   = Component(64, self.ch2, font_size=18, format_string="{0:.2f}")
        self.eev.set_position(28, self.row_3_y)

        self.eeu   = Component(32, self.ch2, font_size=16)
        self.eeu.set_position(92, self.row_3_y)
        self.eeu.set_text(u'\u20AC', x=0, align=0) # Euro

        # Euro total
        self.eti   = Component(self.ch2, self.ch2, font_size=20)
        self.eti.set_position(4, self.row_4_y)
        self.eti.set_text(u'\u03A3', x=0, align=1) # Sigma

        self.etv   = Component(64, self.ch2, font_size=18, format_string="{0:.2f}")
        self.etv.set_position(28, self.row_4_y)

        self.etu   = Component(32, self.ch2, font_size=16)
        self.etu.set_position(92, self.row_4_y)
        self.etu.set_text(u'\u20AC', x=0, align=0) # Euro

        # Add components to the layout
        self.add([self.cdate, self.ctime])
        self.add([self.ewi, self.ewv, self.ewu])
        self.add([self.egi, self.egv, self.egu])
        self.add([self.eei, self.eev, self.eeu])
        self.add([self.eti, self.etv, self.etu])

        self.clear_all()

    def clear_all(self):
        self.ewv.set(0.0)
        self.egv.set(0.0)
        self.eev.set(0.0)
        self.etv.set(0.0)


    def set_date_time(self):
#        tdate = time.strftime('%d-%b-%y')
        self.cdate.set(time.strftime('%d-%b'))
        self.ctime.set(time.strftime('%H:%M'))
        
    def update_total(self):
        self.etv.set(self.ewv.value + self.egv.value + self.eev.value)

if __name__ == '__main__':

    from lcd import LCD

    # Display Layout instance
    L2 = Layout_EUR()

    # Random values for test
    L2.ewv.set(0.3)    
    L2.egv.set(2.64)
    L2.eev.set(0.0)
    L2.update_total()

    # LCD instance
    lcd = LCD(False)       
    lcd.draw(L2)
        
    for i in range(18):
        L2.ewv.add(0.01)
        L2.egv.add(1)
        L2.eev.add(0.17)
        L2.update_total()

        L2.set_date_time()
        lcd.update(L2)

    raw_input()
    
    L2.clear_all()
    lcd.draw(L2)
        
    for i in range(10):
        L2.ewv.add(0.01)
        L2.egv.add(1)
        L2.eev.add(0.17)
        L2.update_total()

        L2.set_date_time()
        lcd.update(L2)

    raw_input()
    lcd.close()
