# -*- coding: utf-8 -*-
import time
from layout import Layout
from layout_222 import Layout_222
from layout_eur import Layout_EUR
from lcd import LCD


class MY_GUI(object):
    def __init__(self):
        L1 = Layout_222()
        L2 = Layout_EUR()

        self.Layout = [L1, L2] # Used when displaying
        self.L_SIZE = len(self.Layout)
        self.L_IDX  = 0
        
        self.L1 = self.Layout[0] # Used when updating data
        self.L2 = self.Layout[1]
        
        self.lcd = LCD(False)
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

    def update_water(self, value):
        self.L1.wv.set(value) # Litter
        self.L2.ewv.set(round(0.0011 * value, 2)) # per Liter

    def update_gas(self, value):
        self.L1.gv.set(value) # m3
        self.L2.egv.set(round(0.80025 * value, 2)) # per m3 (2017-2918)

    def update_electricity(self, value):
        self.L1.ev.set(value) # kWh
        self.L2.eev.set(round(0.24 * value, 2)) # per kW (2017-2918)

    def update_electricity_hour(self, index, value):
        self.L1.egraph.set_bar(index, value) # kWh

    def update_eur_total(self):
        self.L2.update_total()

    def set_date_time(self):
        self.L1.set_date_time()
        self.L2.set_date_time()
        
# ===========================================================
class TEST_MY_GUI(object):
    def __init__(self):
        self.my_gui = MY_GUI()


    def init_some_data(self):
        L1 = self.my_gui.Layout[0]
        L2 = self.my_gui.Layout[1]
        # Random values for test
#        L1.wv.set(890)    
#        L1.gv.set(2.64)
#        L1.ev.set(0.0)

#        L2.ewv.set(0.3)    
#        L2.egv.set(2.64)
#        L2.eev.set(0.0)
#        L2.update_total()

        self.my_gui.update_water(890)
        self.my_gui.update_gas(2.64)
        self.my_gui.update_electricity(0.917)
        self.my_gui.update_eur_total()


    def update_L1(self):
        self.my_gui.L1.egraph.clear_bars()

        for i in range(18):
            self.my_gui.L1.egraph.set_bar(i, i+1)

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
#            self.my_gui.L2.update_total()

            self.my_gui.L2.set_date_time()
            self.my_gui.update_display()    
    

    def run(self):
        self.init_some_data()
        for _ in range(2):
            self.update_L1()
            time.sleep(2)

            self.my_gui.layout_next()
            self.update_L2()
            self.update_L1() # Should not affect the display (shows L2)
            time.sleep(2)
            
            self.my_gui.layout_prev()            
       
        self.my_gui.lcd.close() 
    
    
if __name__ == '__main__':

    my_app = TEST_MY_GUI()
    my_app.run()
