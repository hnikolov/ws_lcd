#!/usr/bin/python
""" This implementation combines 5 python applications:
    - irq water -> send mqtt
    - irq gas   -> send mqtt
    - irq electricity -> send mqtt
    - receive mqtt -> process hour -> send mqtt
    - receive mqtt -> store to file once a day
    It was needed due to strange disconnects 
    (probably caused by the same MAC/IP address?)
"""
import time

from irq_data import IRQ_DATA

def led_on():  print 'default', # default implementation
def led_off(): print '\n' # default implementation


class PROCESS_ALL(object):
    def __init__(self):
        self.w = IRQ_DATA(0)
        self.g = IRQ_DATA(0.0)
        self.e = IRQ_DATA(0.0)

        self.hour  = int(time.strftime('%M'))%24
#        self.hour  = int(time.strftime('%H'))
        self.sdate = time.strftime('%d-%b-%y')
        
        self.mqtt_topic_water       = "power_meter/water"
        self.mqtt_topic_gas         = "power_meter/gas"
        self.mqtt_topic_electricity = "power_meter/electricity"
        self.mqtt_topic_last_will   = "power_meter/status/A"

        self.cleared_mqtt = True
        self.new_day      = False
        
        self.led_on  = led_on
        self.led_off = led_off
        
    def publish(self, topic, data):
        self.led_on()
        time.sleep(0.01)
        print data,
        self.led_off()

    def update_data(self):
        if self.w.update_data() == True:
            self.publish(self.mqtt_topic_water, self.w.get())
            
        if self.g.update_data() == True:
            self.publish(self.mqtt_topic_gas, self.g.get())
            
        if self.e.update_data() == True:
            self.publish(self.mqtt_topic_electricity, self.e.get())


    def update_hour(self, hour):
        self.w.update_hour(hour)
        self.g.update_hour(hour)
        self.e.update_hour(hour)

        self.publish(self.mqtt_topic_water       + '/' + str(hour), self.w.get(hour))
        self.publish(self.mqtt_topic_gas         + '/' + str(hour), self.g.get(hour))
        self.publish(self.mqtt_topic_electricity + '/' + str(hour), self.e.get(hour))


    def clear_mqtt_data(self):
        for h in range(1, 24): # Do not clear 1st-hour data (00:00-01:00)
            self.publish(self.mqtt_topic_water       + '/' + str(h), 0, )
            self.publish(self.mqtt_topic_gas         + '/' + str(h), 0.0)
            self.publish(self.mqtt_topic_electricity + '/' + str(h), 0.0)


    def write_file(self):
        file_name = self.sdate + '.csv'
        with open(file_name, 'w') as fp:
            fp.write(self.sdate + ', W, G, E')
#            for h, (w, g, e) in enumerate(zip(self.h_w, self.h_g, self.h_e)):
#                fp.write(','.join(['\n'+str(h), str(w), str(g), str(e)])) 
            for h in range(24):
                fp.write(','.join(['\n'+str(h), str(self.w.get(h)), str(self.g.get(h)), str(self.e.get(h))]))

    def run(self):
        try:
            while True:
                self.update_data()
                self.update_data() # Extra call, no update expected

                if int(time.strftime('%M'))%24 != self.hour:
                    self.update_hour(self.hour%24)
                    self.hour = int(time.strftime('%M'))%24
                    print self.hour , "-------------------"
                    self.write_file()

                # if int(time.strftime('%H')) != self.hour:
                    # self.update_hour(self.hour)
                    # self.hour = int(time.strftime('%H'))

                if self.hour == 1 and self.cleared_mqtt == False: # New day 01:00 - clear mqtt data
                    self.clear_mqtt_data()
                    self.cleared_mqtt = True
                    self.new_day = False
                    print self.hour

#                if time.strftime('%d-%b-%y') != self.sdate: # New day
                if self.hour == 0 and self.new_day == False:
                    self.new_day = True
                    self.write_file()
                    self.w.clear_data()
                    self.g.clear_data()
                    self.e.clear_data()
                    self.cleared_mqtt = False
                    self.sdate = time.strftime('%d-%b-%y')
                    print self.hour

                time.sleep(1)
                self.w.add( 1 )
                self.g.add( 0.01 )
                self.e.add( 0.001 )
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit, Exception) as e:
            print "Exit...", e


if __name__ == '__main__':
    my_app = PROCESS_ALL()
    my_app.run()
