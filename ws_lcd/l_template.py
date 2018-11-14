# -*- coding: utf-8 -*-
import time
from layout import Layout
from component import *

class LTemplate(Layout):
    def __init__(self, image='plug1.png', unit='kW', format_string="{0:.3f}", ppu=0.18):
        super(LTemplate, self).__init__(color = "black")
        
        self.ch1     = 18 # component height 1
        self.ch2     = 26 # component height 2
        self.sh1     =  2 # separator height 1
        self.bar     = 25

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

#        self.wi   = Component(self.ch2, self.ch2, font_size=20, image='tap-water1.jpg')
        self.wi   = Component(self.ch2, self.ch2, font_size=20, image=image)
        self.wi.set_position(4, self.row_1_y)
#        self.wi.draw_borders()

        self.wv   = Component(68, self.ch2, font_size=18, format_string=format_string)
        self.wv.set_position(30, self.row_1_y)

        self.wu   = Component(self.ch2, self.ch2, font_size=16)
        self.wu.set_position(98, self.row_1_y)
        self.wu.set_text(unit, 0, align=0)

#        self.gi   = Component(self.ch2, self.ch2, font_size=20, image='gas_32x32.png')
        self.gi   = Component(self.ch2, self.ch2, font_size=19)
        self.gi.set_position(4, self.row_2_y)
        self.gi.set_text(u'\u03A3', x=0, align=1) # Sigma
        
        self.gv   = Component(68, self.ch2, font_size=18, format_string="{0:.2f}")
        self.gv.set_position(30, self.row_2_y)

        self.gu   = Component(self.ch2, self.ch2, font_size=16)
        self.gu.set_position(98, self.row_2_y)
#        self.gu.set_text("m" + u'\u00B3', 0, align=0)
        self.gu.set_text(u'\u20AC', x=0, align=0) # Euro 

#        self.ei   = Component(self.ch2, self.ch2, font_size=20, image='plug1.png')
        self.ei   = Component(self.ch2, self.ch2, font_size=17, bg_color=0)
        self.ei.set_position(4, self.row_3_y)
        self.ei.set_text("12h", align=1)

        self.ev   = Component(68, self.ch2, font_size=17, format_string=format_string, bg_color=0)
        self.ev.set_position(30, self.row_3_y)

        self.eu   = Component(self.ch2, self.ch2, font_size=16, bg_color=0)
        self.eu.set_position(98, self.row_3_y)
        self.eu.set_text(unit, 0, align=0)

        self.egraph = BarGraph(128, self.bar, bg_color=0)
        self.egraph.set_position(2, self.row_4_y)
        self.egraph.update()
        # --------------------------------------------------

        # Add components to the layout
        self.add([self.cdate, self.ctime])
        self.add([self.wi, self.wv, self.wu])
        self.add([self.gi, self.gv, self.gu])
        self.add([self.ei, self.ev, self.eu])
        self.add([self.egraph])

        self.clear_all()

    def clear_all(self):
        self.wv.set(0)
        self.gv.set(0.0)
        self.ev.set(0.0)
        self.egraph.clear_bars()


    def set_date_time(self):
#        tdate = time.strftime('%d-%b-%y')
        self.cdate.set(time.strftime('%d-%b'))
        self.ctime.set(time.strftime('%H:%M'))
        

if __name__ == '__main__':

    from lcd import LCD

    # Display Layout instance
#    L2 = LTemplate(image='tap-water1.jpg', unit='Lit', format_string="{}")
#    L2 = LTemplate(image='gas_32x32.png', unit="m" + u'\u00B3', format_string="{0:.2f}")
    L2 = LTemplate(image='plug1.png', unit='kW', format_string="{0:.3f}")

    # Random values for test
    L2.wv.set(1.890)    
    L2.gv.set(2.64)
    L2.ev.set(0.0)

    # LCD instance
    lcd = LCD(False)       
    lcd.draw(L2)

    for i in range(18):
        L2.egraph.set_bar(i, i+1)
        L2.set_date_time()
        lcd.update(L2)
        
    L2.egraph.set_bar(23,12.0)
        
    for i in range(5):
        L2.wv.add(0.001)
        L2.gv.add(0.01)
        L2.ev.add(0.001)

        L2.set_date_time()
        L2.egraph.set_bar(18+i, 12 - (4 + i))
        lcd.update(L2)

    raw_input()
    
    L2.clear_all()
    lcd.draw(L2)
    lcd.close()
