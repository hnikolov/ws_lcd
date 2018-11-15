#!/usr/bin/python
import paho.mqtt.client as mqtt
import datetime, sys
import time
from layout_mix import MY_GUI

MQTT_SERVER = "192.168.2.100"


class FILE_LOGGER():
    """ Log data received via mqtt to files """
    def __init__(self):
        self.data_w = ['-'] * 24 # per hour
        self.data_g = ['-'] * 24
        self.data_e = ['-'] * 24
        
        self.dconn = 0        
        self.mqtt_topic_electricity = "power_meter/electricity/#"
        self.mqtt_topic_temperature = "power_meter/temperature/#"
        self.mqtt_topic_water       = "power_meter/water/#"
        self.mqtt_topic_gas         = "power_meter/gas/#"
        self.mqtt_topic_last_will   = "power_meter/status/F"        

        self.mqtt_client = mqtt.Client()

        self.mqtt_client.will_set(topic = self.mqtt_topic_last_will, payload="offline", qos=self.QoS, retain=True)
        self.mqtt_client.on_connect     = self.on_connect
        self.mqtt_client.on_message     = self.on_message
        self.mqtt_client.on_disconnect  = self.on_disconnect

        self.mqtt_client.connect(MQTT_SERVER, 1883, 60)


    # MQTT handler ===============================================================================
    def on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server.
            Subscribing in on_connect() means that if we lose the connection and
            reconnect then subscriptions will be renewed.
        """
        if rc == 0:
#            client.subscribe("power_meter/status/#") # To log number of disconnects?
            client.subscribe(self.mqtt_topic_gas)
            client.subscribe(self.mqtt_topic_water)
            client.subscribe(self.mqtt_topic_electricity)
            print "Connected to: " + MQTT_SERVER
            self.mqtt_client.publish(self.mqtt_topic_last_will, "online, " + str(self.dconn), self.QoS, self.retain)
        print "Result code:", rc

    def on_disconnect(self, client, userdata, msg):
        """ The callback for when disconnect from the server. """
        self.dconn += 1
        
    def on_message(self, client, userdata, msg):
        """ The callback for when a PUBLISH message is received from the server. """
        st = datetime.datetime.fromtimestamp(msg.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
        print st[:-3],  ":", msg.topic, ":", msg.payload
            
        if msg.topic == self.mqtt_topic_water:
            self.my_gui.update_water(int(msg.payload)) # Litter
            
        elif self.mqtt_topic_water in msg.topic: 
            index = int(msg.topic.split('/')[-1])
            self.data_w[index] = msg.payload
            
        # -----------------------------------------------------------------
        elif msg.topic == self.mqtt_topic_gas:
            self.my_gui.update_gas(float(msg.payload)) # m3, 10 Litters/msg
            
        elif self.mqtt_topic_gas in msg.topic:
            index = int(msg.topic.split('/')[-1])
            self.data_g[index] = msg.payload
            
        # -----------------------------------------------------------------
        elif msg.topic == self.mqtt_topic_electricity:
            self.my_gui.update_electricity(float(msg.payload)) # kWh
            
        elif self.mqtt_topic_electricity in msg.topic: # covers /1 /2 ... etc.
            index = int(msg.topic.split('/')[-1])
            self.data_e[index] = msg.payload

    def write_file(self):
        file_name = self.sdate + '.csv'
        
        with open(file_name, 'w') as fp:
            fp.write(self.sdate + ', W, G, E')
            for h, (w, g, e) in enumerate(zip(self.data_w, self.data_g, self.data_e)):
                fp.write(','.join(str(h), w, g, e)

        for i in range(24):
            self.data_w[i] = ['-']
            self.data_g[i] = ['-']
            self.data_e[i] = ['-']                
        
    def run(self):
        try:
            self.mqtt_client.loop_start()
            while True:               
                if int(time.strftime('%H')) == 0: # New day
                    time.sleep(30) # Give time to receive the last hour data
                    self.write_file()
                    time.sleep(3600) # Till next hour, so write only once a day. TODO?
                time.sleep(1)
                
        except (KeyboardInterrupt, SystemExit, Exception) as e:
            print "Exit...", e
            self.mqtt_client.loop_stop()


# ============================================================================================
if __name__ == '__main__':
    myApp = FILE_LOGGER()
    myApp.run()

