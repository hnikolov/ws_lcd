# -*- coding: utf-8 -*-
import time
from layout import Layout
from component import *
from darksky import DarkSky

class LWeather(Layout):
    def __init__(self):
        super(LWeather, self).__init__(color = "black")

        self.ds = DarkSky()
        self.last_temperature = 20.0
        
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

        # N/A: u'\uf07b'

        # Build the layout
        self.mi = Component(self.ch2, self.ch2, font='weathericons-regular-webfont.ttf', font_size=14, bg_color=0, align=1)
        self.mi.set_position(2, 0)
        self.mi.set_text(u'\uF0E2') # Moon phase, TODO use the 28 icons

        self.cdate = Component(52, self.ch2, font_size=14, bg_color=0, align=1)
        self.cdate.set_position(20, 0)
        self.cdate.set(time.strftime('%d-%b'))

        self.ctime = Component(56, self.ch2, font_size=14, bg_color=0, align=1)
        self.ctime.set_position(72, 0)
        self.ctime.set(time.strftime('%H:%M'))
        # ----------------
        self.tv = Component(48, 2*self.ch2, font_size=24, format_string = "{0:.0f}" + u'\N{DEGREE SIGN}', align=1)
        self.tv.set_position(0, self.row_1_y)
        self.tv.set(-23.45)

        self.ti = Component(48, 2*self.ch2, font='weathericons-regular-webfont.ttf', font_size=26, align=1, bg_color=255)
        self.ti.set_position(44, self.row_1_y)
        self.ti.set_text(u'\uF002') # Weather icon

        self.tmax = Component(34, self.ch2, font_size=14, format_string = "{0:.0f}" + u'\N{DEGREE SIGN}', align=2)
        self.tmax.set_position(94, self.row_1_y)
        self.tmax.set(-18.87)

        self.tmin = Component(34, self.ch2, font_size=14, format_string = "{0:.0f}" + u'\N{DEGREE SIGN}', align=2)
        self.tmin.set_position(94, self.row_1_y + self.ch2)
        self.tmin.set(-27.64)
        # -----------------------------
        self.ln = Component(92, self.ch2, font_size=13, font='Roboto-Condensed.ttf', align=1)
        self.ln.set_position(0, self.row_2_y)
        self.ln.set_text("Valkenburg, ZH")

        self.td = Component(34, self.ch2, font_size=22, font='weathericons-regular-webfont.ttf', align=1) # temperature direction
        self.td.set_position(94, self.row_2_y)
        self.td.set_text(u'\uF058') # Arrow up: f058, down: f044
        # -------------------------------------
        self.hi = Component(self.ch2, self.ch2, font='weathericons-regular-webfont.ttf', font_size=16, bg_color=0)
        self.hi.set_position(0, self.row_3_y)
        self.hi.set_text(u'\uF07A', align=1) # Humidity, Water drop: u'\uF078'

        self.hv = Component(44, self.ch2, font_size=18, font='Roboto-Condensed.ttf', format_string = "{0:.0f}%", align=0, bg_color=0)
        self.hv.set_position(20, self.row_3_y)
        self.hv.set(67)

        self.ri = Component(24, self.ch2, font='weathericons-regular-webfont.ttf', font_size=16, bg_color=0)
        self.ri.set_position(66, self.row_3_y)
        self.ri.set_text(u'\uF084', align=1) # Umbrella

        self.rv = Component(38, self.ch2, font_size=18, font='Roboto-Condensed.ttf', format_string = "{0:.0f}%", align=0, bg_color=0)
        self.rv.set_position(90, self.row_3_y)
        self.rv.set(26.32)

        self.pi = Component(self.ch2, self.ch2, font_size=18, font='weathericons-regular-webfont.ttf', bg_color=0)
        self.pi.set_position(0, self.row_4_y)
        self.pi.set_text(u'\uF079', x=0, align=1) # Barometer

        self.pv = Component(64, self.ch2, font_size=18, format_string="{0:.1f}", align=0, bg_color=0)
        self.pv.set_position(20, self.row_4_y)
        self.pv.set(1023.52)

        self.wi = Component(34, self.ch2, font='weathericons-regular-webfont.ttf', font_size=20, bg_color=0, align=0)
        self.wi.set_position(94, self.row_4_y)
        self.wi.set_text(u'\uF0B7') # Wind

        # Add components to the layout
        self.add([self.mi, self.cdate, self.ctime])
        self.add([self.tv, self.ti, self.tmax, self.tmin])
        self.add([self.ln, self.td])
        self.add([self.hi, self.hv, self.ri, self.rv])
        self.add([self.pi, self.pv, self.wi])

#        self.update()


    def set_date_time(self):
        if self.ctime.get()[:2] != time.strftime('%H'):
           self.update()
        
        self.cdate.set(time.strftime('%d-%b'))
        self.ctime.set(time.strftime('%H:%M'))
        
    def update(self):
        self.ds.request()
        
        self.mi.set_text(self.ds.get_icon_moon())
        self.ti.set_text(self.ds.get_icon_weather())
        self.tmax.set(self.ds.get_apparent_temperature_high())
        self.tmin.set(self.ds.get_apparent_temperature_low())
        self.ln.set_text(self.ds.get_location())
        self.hv.set(self.ds.get_humidity())
        self.rv.set(self.ds.get_chances_rain())
        self.pv.set(self.ds.get_pressure())
        self.wi.set_text(self.ds.get_icon_wind())
        
        current_temperature = self.ds.get_apparent_temperature()
        self.tv.set(current_temperature)
        
        if current_temperature > self.last_temperature + 1:
            self.td.set_text(u'\uF058') # Arrow up
        
        elif current_temperature < self.last_temperature - 1:
            self.td.set_text(u'\uF044') # Arrow down
        
        self.last_temperature = self.ds.get_apparent_temperature()
        


if __name__ == '__main__':

    from lcd import LCD

    # Display Layout instance
    L2 = LWeather()

    # LCD instance
    lcd = LCD(False)
    lcd.draw(L2)
    
    L2.update()
    lcd.draw(L2)

    raw_input()
    lcd.close()
