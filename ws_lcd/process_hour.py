#!/usr/bin/python
import paho.mqtt.client as mqtt
#import datetime, sys
import time

MQTT_SERVER = "192.168.2.100"

class ProcessHourData(object):
    def __init__(self):
        self.h_w  = [0]   * 24
        self.h_g  = [0.0] * 24
        self.h_e  = [0.0] * 24
        self.hour = int(time.strftime('%H'))
        self.hts  = self.hour # hour to send
        
        self.l_w = 0 # TODO: delta Last received water: int(msg.payload) - l_w
        
        self.not_published_yet = False
        self.not_cleared_yet   = False        

        self.connected = False
        self.dconn     = 0
        self.QoS       = 0 # or 2?
        self.retain    = True

        self.mqtt_topic_water       = "power_meter/water"
        self.mqtt_topic_gas         = "power_meter/gas"
        self.mqtt_topic_electricity = "power_meter/electricity"
        self.mqtt_topic_last_will   = "power_meter/status/H"

        self.mqtt_client = mqtt.Client(client_id="process_hour")

        # To use the will message at the EDP side, subscribe to topic power_meter/status
        self.mqtt_client.will_set(topic = self.mqtt_topic_last_will, payload="offline", qos=self.QoS, retain=True)
        self.mqtt_client.on_connect     = self.on_connect
        self.mqtt_client.on_message     = self.on_message
        self.mqtt_client.on_disconnect  = self.on_disconnect

        self.mqtt_client.connect(MQTT_SERVER, 1883, 60)

    # MQTT handler ===============================================================================
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(self.mqtt_topic_gas)
            client.subscribe(self.mqtt_topic_water)
            client.subscribe(self.mqtt_topic_electricity)
            self.connected = True
            print "Connected to: " + MQTT_SERVER
            self.mqtt_client.publish(self.mqtt_topic_last_will, "online, " + str(self.dconn), self.QoS, self.retain)
        print "Result code:", rc

    def on_message(self, client, userdata, msg):
        """ The callback for when a PUBLISH message is received from the server. """
        if msg.topic == self.mqtt_topic_water:
            self.h_w[self.hour] += 1     # Liter

        elif msg.topic == self.mqtt_topic_gas:
            self.h_g[self.hour] += 0.01  # m3, 10 Litters/msg

        elif msg.topic == self.mqtt_topic_electricity: 
            self.h_e[self.hour] += 0.001 # kWh
            

    def on_disconnect(self, client, userdata, msg):
        """ The callback for when disconnect from the server. """
        print "Disconnected:", msg
        self.connected == False
        self.dconn     += 1
    # ===============================================================================    

    def publish_data(self, hour):
        if self.connected == True:
            self.mqtt_client.publish(self.mqtt_topic_water       + '/' + str(hour), self.h_w[hour], self.QoS, self.retain)    
            self.mqtt_client.publish(self.mqtt_topic_gas         + '/' + str(hour), self.h_g[hour], self.QoS, self.retain)    
            self.mqtt_client.publish(self.mqtt_topic_electricity + '/' + str(hour), self.h_e[hour], self.QoS, self.retain) 
            self.not_sent_yet = False
        else:
            self.not_sent_yet = True        


    def clear_mqtt_data(self):
        if self.connected == True:
            for h in range(1, 24): # Keep the data from 00:00-01:00
                self.mqtt_client.publish(self.mqtt_topic_water       + '/' + str(h), 0,   self.QoS, self.retain)    
                self.mqtt_client.publish(self.mqtt_topic_gas         + '/' + str(h), 0.0, self.QoS, self.retain)    
                self.mqtt_client.publish(self.mqtt_topic_electricity + '/' + str(h), 0.0, self.QoS, self.retain)
                
                time.sleep(0.01) # Is needed?
                self.not_cleared_yet = False
        else:
            self.not_cleared_yet = True       
            
            
    def run(self):
        try:
            self.mqtt_client.loop_start()
            while True:
                if self.not_published_yet: # In case of disconnect
                    self.publish_data(self.hts)
                
                if self.not_cleared_yet: # In case of disconnect            
                    self.clear_mqtt_data()    # Must happen between 01:00 and 01:59
                
                if int(time.strftime('%H')) != self.hour:
                    self.hts  = self.hour # It has up to 1 hour in case of disconnect
                    self.hour = int(time.strftime('%H'))
                    self.h_w[self.hour] = 0
                    self.h_g[self.hour] = 0.0
                    self.h_e[self.hour] = 0.0
                    self.publish_data(self.hts)
                                    
                if self.hour == 1: # New day 01:00 - clear data
                    self.clear_mqtt_data()
                    
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit, Exception) as e:
            print "Exit...", e
            self.mqtt_client.loop_stop()
            
        
if __name__ == '__main__':
    my_app = ProcessHourData()
    my_app.run()
