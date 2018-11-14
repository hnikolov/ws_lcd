# -*- coding: utf-8 -*-
import time
from layout import Layout
from component import *

class LEnergy(Layout):
    def __init__(self):
        super(LEnergy, self).__init__(color = "black")
        
        self.ch1     = 20 # component height 1
        self.ch2     = 30 # component height 2
        self.sh1     =  4 # separator height 1

        # Offsets
        self.row_1_y = self.ch1
        self.sep_2_y = self.row_1_y + self.ch2
        self.row_2_y = self.sep_2_y + self.sh1
        self.sep_3_y = self.row_2_y + self.ch2
        self.row_3_y = self.sep_3_y + self.sh1
        self.sep_4_y = self.row_3_y + self.ch2
        self.row_4_y = self.sep_4_y + self.sh1

        # Build the layout
        self.cdate   = Component(72, self.ch1, font_size=14, bg_color=0, align=1)
        self.cdate.set_position(0, 0)
        self.cdate.set(time.strftime('%d-%b'))

        self.ctime   = Component(56, self.ch1, font_size=14, bg_color=0, align=1)
        self.ctime.set_position(72, 0)
        self.ctime.set(time.strftime('%H:%M'))
#        self.ctime.draw_borders()

        self.wi   = Component(self.ch2, self.ch2, iw=26, ih=26, image='tap-water1.jpg')
        self.wi.set_position(4, self.row_1_y)

        self.wv   = Component(68, self.ch2, font_size=19)
        self.wv.set_position(30, self.row_1_y)

        self.wg   = BarGraph(self.ch2, self.ch2, bg_color=255)
        self.wg.set_position(98, self.row_1_y)

        # --------------------------------------------------------------------------
        self.gi   = Component(self.ch2, self.ch2, iw=26, ih=26, image='gas_32x32.png')
        self.gi.set_position(4, self.row_2_y)

        self.gv   = Component(68, self.ch2, font_size=19, format_string="{0:.2f}")
        self.gv.set_position(30, self.row_2_y)

        self.gg   = BarGraph(self.ch2, self.ch2, bg_color=255)
        self.gg.set_position(98, self.row_2_y)

        # --------------------------------------------------------------------------
        self.ei   = Component(self.ch2, self.ch2, iw=26, ih=26, image='plug1.png')
        self.ei.set_position(4, self.row_3_y)
        
        self.ev   = Component(68, self.ch2, font_size=19, format_string="{0:.3f}")
        self.ev.set_position(30, self.row_3_y)
                
        self.eg   = BarGraph(self.ch2, self.ch2, bg_color=255)
        self.eg.set_position(98, self.row_3_y)

        # Add components to the layout
        self.add([self.cdate, self.ctime])
        self.add([self.wi, self.wv, self.wg])
        self.add([self.gi, self.gv, self.gg])
        self.add([self.ei, self.ev, self.eg])

        self.clear_all()

    def clear_all(self):
        self.wv.set(0)
        self.gv.set(0.0)
        self.ev.set(0.0)
        self.eg.clear_bars()


    def set_date_time(self):
        self.cdate.set(time.strftime('%d-%b'))
        self.ctime.set(time.strftime('%H:%M'))
        

if __name__ == '__main__':

    from lcd import LCD

    # Display Layout instance
    L2 = LEnergy()

    # Random values for test
    L2.wv.set(890)    
    L2.gv.set(2.64)
    L2.ev.set(0.0)

    # LCD instance
    lcd = LCD(False)       
    lcd.draw(L2)

    for i in range(18):
        L2.eg.set_bar(i, i+1)
        L2.set_date_time()
        lcd.update(L2)
#        raw_input()
        
    L2.eg.set_bar(23,12.0)
        
    for i in range(5):
        L2.wv.add(1)
        L2.gv.add(0.01)
        L2.ev.add(0.001)

        L2.set_date_time()
        L2.eg.set_bar(18+i, 12 - (4 + i))
        lcd.update(L2)

    raw_input()
    
    L2.clear_all()
    lcd.draw(L2)
        
    idx = 0
    for j in range(4):   
        for i in range(6):
            L2.wv.add(1)
            L2.gv.add(0.01)
            L2.set_date_time()
            L2.eg.set_bar(idx, float(2.11*(i+1)))
#            print float(2.11*(i+1))
            lcd.update(L2)
            idx += 1
            raw_input()
        
    lcd.close()
