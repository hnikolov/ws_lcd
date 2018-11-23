#!/usr/bin/python
import time

class IRQ_DATA(object):
    def __init__(self, default):
        self.h_w = [default] * 24
        self.w   =  default  # Updated (+1) by irq
        self.lw  =  default  # Last sent
        self.phw =  default  # Previous hour total

        self.default = default # 0 or 0.0

    def add(self, value):
        self.w += value
        
    def update_data(self):
        if self.lw != self.w:
            self.lw = self.w
            return True
        return False


    def update_hour(self, hour):
        self.h_w[hour] = self.w - self.phw
        self.phw = self.w


    def clear_data(self):
        for i in range(24):
            self.h_w[i] = default

        self.w   = default # Updated by irq
        self.lw  = default # Last sent
        self.phw = default # Previous hour total


    def get(self, hour = None):
        if hour == None:
            return self.lw
        return self.w[hour]
