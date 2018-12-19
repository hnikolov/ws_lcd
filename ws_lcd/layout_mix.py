# -*- coding: utf-8 -*-
import time
from layout import Layout
from l_energy import LEnergy
from l_template import LTemplate
from layout_eur import Layout_EUR
from l_weather import LWeather
from lcd import LCD


class MY_GUI(object):
    def __init__(self, WS = False):
        L1 = LEnergy()
        L2 = Layout_EUR()
        L3 = LTemplate(image='tap-water1.jpg', unit='Lit', format_string="{}", ppu=0.0011)
        L4 = LTemplate(image='gas_32x32.png', unit="m" + u'\u00B3', format_string="{0:.2f}", ppu=0.80025)
        L5 = LTemplate(image='plug1.png', unit='kW', format_string="{0:.3f}", ppu=0.24)
        L6 = LWeather()

        self.Layout = [L1, L2, L3, L4, L5, L6] # Used when displaying
        self.L_SIZE = len(self.Layout)
        self.L_IDX  = 0
        
        self.L1 = self.Layout[0] # Ref used when updating data
        self.L2 = self.Layout[1] # Eur
        self.L3 = self.Layout[2] # Water
        self.L4 = self.Layout[3] # Gas
        self.L5 = self.Layout[4] # Electricity
        self.L6 = self.Layout[5] # Weather
        
        self.lcd = LCD(WS)
        self.draw_display()
   
    def draw_display(self):
        self.lcd.draw(self.Layout[self.L_IDX])

    def update_display(self):
        self.lcd.update(self.Layout[self.L_IDX])

    def layout_next(self):
        self.L_IDX = (self.L_IDX + 1) % self.L_SIZE
        self.draw_display()

    def layout_prev(self):
        self.L_IDX = (self.L_IDX - 1) % self.L_SIZE
        self.draw_display()

    # TODO: duplicate ppu
    def update_water(self, value):
        self.L1.wv.set(value) # Litter
        self.L2.ewv.set(round(0.0011 * value, 2)) # per Liter
        self.L3.update(value)

    def update_water_hour(self, index, value):
        self.L1.wg.set_bar(index, value) # Liters
        self.L3.update_hour_data(index, value)

    def update_gas(self, value):
        self.L1.gv.set(value) # m3
        self.L2.egv.set(round(0.80025 * value, 2)) # per m3 (2017-2918)
        self.L4.update(value)

    def update_gas_hour(self, index, value):
        self.L1.gg.set_bar(index, value) # Liters
        self.L4.update_hour_data(index, value)

    def update_electricity(self, value):
        self.L1.ev.set(value) # kWh
        self.L2.eev.set(round(0.24 * value, 2)) # per kW (2017-2918)
        self.L5.update(value)

    def update_electricity_hour(self, index, value):
        self.L1.eg.set_bar(index, value) # kWh
        self.L5.update_hour_data(index, value)

    def update_eur_total(self):
        self.L2.update_total()

    def set_date_time(self):
        self.L1.set_date_time()
        self.L2.set_date_time()
        self.L3.set_date_time()
        self.L4.set_date_time()
        self.L5.set_date_time()
        self.L6.set_date_time()
        
    def hour_data_next(self):
        self.L3.hour_data_next()
        self.L4.hour_data_next()
        self.L5.hour_data_next()
        self.update_display()

    def hour_data_prev(self):
        self.L3.hour_data_prev()
        self.L4.hour_data_prev()
        self.L5.hour_data_prev()
        self.update_display()

# ===========================================================
class TEST_MY_GUI(object):
    def __init__(self):
        self.my_gui = MY_GUI()


    def init_some_data(self):
        L1 = self.my_gui.Layout[0]
        L2 = self.my_gui.Layout[1]
        # Random values for test
        self.my_gui.update_water(890)
        self.my_gui.update_gas(2.64)
        self.my_gui.update_electricity(0.917)
        self.my_gui.update_eur_total()


    def update_L1(self):
        self.my_gui.L1.wg.clear_bars()
        self.my_gui.L1.gg.clear_bars()
        self.my_gui.L1.eg.clear_bars()

        for i in range(18):
            self.my_gui.update_water_hour(i, i+1)
            self.my_gui.update_gas_hour(i, i*2)
            self.my_gui.update_electricity_hour(i, i*3)

            self.my_gui.L1.wv.add(1)
            self.my_gui.L1.gv.add(0.01)
            self.my_gui.L1.ev.add(0.001)

            self.my_gui.L1.set_date_time()
            self.my_gui.update_display()
    
    
    def update_L2(self):
        for i in range(18):
            self.my_gui.L2.ewv.add(0.01)
            self.my_gui.L2.egv.add(1)
            self.my_gui.L2.eev.add(0.17)
            self.my_gui.update_eur_total()

            self.my_gui.L2.set_date_time()
            self.my_gui.update_display()    
    

    def run(self):
        self.init_some_data()
        for _ in range(2):
            self.update_L1()
            time.sleep(1)

            self.my_gui.layout_next()
            self.update_L2()
            self.update_L1() # Should not affect the display (shows L2)
            time.sleep(1)
            
            self.my_gui.layout_prev()            
       
        # Show all screens
        for _ in range(10):
            time.sleep(1)
            self.my_gui.layout_next()

        # Show hour data above the bar graph
        self.my_gui.L_IDX = 2
        self.my_gui.draw_display()
        for _ in range(10):
            self.my_gui.hour_data_next()
            time.sleep(.3)

        self.my_gui.L_IDX = 3
        self.my_gui.draw_display()
        for _ in range(10):
            self.my_gui.hour_data_prev()
            time.sleep(.3)

        self.my_gui.lcd.close() 
    
    
if __name__ == '__main__':

    my_app = TEST_MY_GUI()
    my_app.run()
