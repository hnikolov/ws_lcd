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
import paho.mqtt.client as mqtt
import time

from log import LOG
from irq_data import IRQ_DATA

def led_on():  print 'default', # default implementation
def led_off(): print '\n'

MQTT_SERVER = "192.168.2.100"

class PROCESS_ALL(object):
    def __init__(self):
        self.L = LOG()
        
        self.w = IRQ_DATA(0)
        self.g = IRQ_DATA(0.0)
        self.e = IRQ_DATA(0.0)

        self.hour  = int(time.strftime('%H'))
        self.sdate = time.strftime('%d-%b-%y')

        self.led_on  = led_on
        self.led_off = led_off

        self.connected    = False
        self.dconn        = 0
        self.QoS          = 0 # or 2?
        self.retain       = True
        self.cleared_mqtt = False

        self.mqtt_topic_water       = "power_meter/water"
        self.mqtt_topic_gas         = "power_meter/gas"
        self.mqtt_topic_electricity = "power_meter/electricity"
        self.mqtt_topic_last_will   = "power_meter/status/A"

        self.mqtt_client = mqtt.Client(client_id="process_all")

        # To use the will message at the EDP side, subscribe to topic power_meter/status
        self.mqtt_client.will_set(topic = self.mqtt_topic_last_will, payload="offline", qos=self.QoS, retain=True)
        self.mqtt_client.on_connect     = self.on_connect
        self.mqtt_client.on_disconnect  = self.on_disconnect
        self.mqtt_client.on_publish     = self.on_publish
        self.mqtt_client.on_log         = self.on_log

    # MQTT handler ===============================================================================
    def on_log(client, userdata, level, buf):
        self.L.log(buf)
        if "PINGRESP" in buf:
            self.connected = True
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            self.L.log("Connected to: " + MQTT_SERVER)
            self.led_off()
            self.mqtt_client.publish(self.mqtt_topic_last_will, "online, " + str(self.dconn), self.QoS, self.retain)
        self.L.log("Result code: " + str(rc))

    def on_disconnect(self, client, userdata, msg):
        """ The callback for when disconnect from the server. """
        self.L.log("Disconnected: " + msg)
        self.connected = False
        self.dconn    += 1
        self.led_off()

    def on_publish(self, client, userdata, mid):
        self.led_off()
    # ===============================================================================

    def connect(self):
        try:
            self.led_on()
            self.mqtt_client.loop_stop() # Stop also auto reconnects
            self.mqtt_client.connect(MQTT_SERVER, 1883, 60)
            self.mqtt_client.loop_start()
            while not self.connected:
                time.sleep(2)

        except Exception:
            self.L.log(traceback.format_exc())
            time.sleep(4)

    def publish(self, topic, data):
        self.led_on()
        self.mqtt_client.publish(topic, data, self.QoS, self.retain)
        time.sleep(0.05)

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
            for h in range(24):
                fp.write(','.join(['\n'+str(h), str(self.w.get(h)), str(self.g.get(h)), str(self.e.get(h))]))


    def run(self):
        try:
            self.connect()
            while True:
                if self.connected == False:
                    self.connect()
                else:
                    self.update_data()

                    if int(time.strftime('%H')) != self.hour:
                        self.update_hour(self.hour)
                        self.hour = int(time.strftime('%H'))

                    if self.hour == 1 and self.cleared_mqtt == False: # New day 01:00 - clear mqtt data
                        self.clear_mqtt_data()
                        self.cleared_mqtt = True

                    if time.strftime('%d-%b-%y') != self.sdate: # New day
                        self.write_file()
                        self.w.clear_data()
                        self.g.clear_data()
                        self.e.clear_data()
                        self.cleared_mqtt = False
                        self.sdate = time.strftime('%d-%b-%y')

                    time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            self.L.log("Exit...")

        except (Exception) as e:
            self.L.log(traceback.format_exc())
            
        finally:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()

            
if __name__ == '__main__':
    my_app = PROCESS_ALL()
    my_app.run()
