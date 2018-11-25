#!/usr/bin/python
import time


class IRQ_DATA(object):
    def __init__(self, default):
        self.h_v = [default] * 24 # Per hour
        self.v   =  default       # Updated by irq
        self.lv  =  default       # Last sent
        self.phv =  default       # Previous hour total

        self.default = default # 0 or 0.0


    def add(self, value):
        self.v += value
        

    def update_data(self):
        if self.lv != self.v:
            self.lv = self.v
            return True
        return False


    def update_hour(self, hour):
        self.h_v[hour] = self.v - self.phv
        self.phv = self.v


    def clear_data(self):
        for i in range(24):
            self.h_v[i] = self.default

        self.v   = self.default # Updated by irq
        self.lv  = self.default # Last sent
        self.phv = self.default # Previous hour total


    def get(self, hour = None):
        if hour == None:
            return self.lv
        return self.h_v[hour]
