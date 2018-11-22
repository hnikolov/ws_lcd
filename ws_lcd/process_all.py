#!/usr/bin/python
import paho.mqtt.client as mqtt
import time

MQTT_SERVER = "192.168.2.100"

class PROCESS_ALL(object):
    def __init__(self):
        self.h_w = [0]   * 24
        self.h_g = [0.0] * 24
        self.h_e = [0.0] * 24

        self.hour  = int(time.strftime('%H'))
        self.sdate = time.strftime('%d-%b-%y')
        
        self.w  = 0   # Updated (+1) by irq
        self.lw = 0   # Last sent water
        self.g  = 0.0 # Updated (+0.01) by irq  
        self.lg = 0.0 # Last sent gas
        self.e  = 0.0 # Updated (+0.001) by irq
        self.le = 0.0 # Last sent electricity

        self.connected = False
        self.dconn     = 0
        self.QoS       = 0 # or 2?
        self.retain    = True

        self.mqtt_topic_water       = "power_meter/water"
        self.mqtt_topic_gas         = "power_meter/gas"
        self.mqtt_topic_electricity = "power_meter/electricity"
        self.mqtt_topic_last_will   = "power_meter/status/A"

        self.mqtt_client = mqtt.Client(client_id="process_all")

        # To use the will message at the EDP side, subscribe to topic power_meter/status
        self.mqtt_client.will_set(topic = self.mqtt_topic_last_will, payload="offline", qos=self.QoS, retain=True)
        self.mqtt_client.on_connect     = self.on_connect
        self.mqtt_client.on_disconnect  = self.on_disconnect
     
    # MQTT handler ===============================================================================
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print "Connected to: " + MQTT_SERVER
            self.mqtt_client.publish(self.mqtt_topic_last_will, "online, " + str(self.dconn), self.QoS, self.retain)
        print "Result code:", rc
            
    def on_disconnect(self, client, userdata, msg):
        """ The callback for when disconnect from the server. """
        print "Disconnected:", msg
        self.connected == False
        self.dconn     += 1
    # ===============================================================================    

    def connect(self):
        self.mqtt_client.loop_stop() # Stop also auto reconnects
        self.mqtt_client.connect(MQTT_SERVER, 1883, 60)
        self.mqtt_client.loop_start()
        while not self.connected:
            print "Connecting..."
            time.sleep(1)
        

    def update_data():
        if self.lw != self.w:
            self.lw = self.w
            self.mqtt_client.publish(self.mqtt_topic_water, self.lw, self.QoS, self.retain) 
            
        if self.lg != self.g:
            self.lg = self.g
            self.mqtt_client.publish(self.mqtt_topic_gas, self.lg, self.QoS, self.retain) 
            
        if self.le != self.e:
            self.le = self.e
            self.mqtt_client.publish(self.mqtt_topic_electricity, self.le, self.QoS, self.retain) 
            
            
    def update_hour(self, hour):
        self.h_w[hour] = self.w if hour == 0 else self.w - self.h_w[hour - 1]
        self.h_g[hour] = self.g if hour == 0 else self.g - self.h_g[hour - 1]
        self.h_e[hour] = self.e if hour == 0 else self.e - self.h_e[hour - 1]        
        
        self.mqtt_client.publish(self.mqtt_topic_water       + '/' + str(hour), self.h_w[hour], self.QoS, self.retain)    
        self.mqtt_client.publish(self.mqtt_topic_gas         + '/' + str(hour), self.h_g[hour], self.QoS, self.retain)    
        self.mqtt_client.publish(self.mqtt_topic_electricity + '/' + str(hour), self.h_e[hour], self.QoS, self.retain) 


    def clear_mqtt_data(self):
        for h in range(1, 24): # Do not clear 1st-hour data (00:00-01:00)
            self.mqtt_client.publish(self.mqtt_topic_water       + '/' + str(h), 0,   self.QoS, self.retain)    
            self.mqtt_client.publish(self.mqtt_topic_gas         + '/' + str(h), 0.0, self.QoS, self.retain)    
            self.mqtt_client.publish(self.mqtt_topic_electricity + '/' + str(h), 0.0, self.QoS, self.retain)    
            time.sleep(0.01) # Is needed?


    def write_file(self):
        file_name = self.sdate + '.csv'       
        with open(file_name, 'w') as fp:
            fp.write(self.sdate + ', W, G, E')
            for h, (w, g, e) in enumerate(zip(self.h_w, self.h_g, self.h_e)):
                fp.write(','.join(['\n'+str(h), str(w), str(g), str(e)]))      

    
    def run(self):
        try:
            self.connect()
            while True:
                if self.connected == False:
                    self.connect() # We should not need this
                else:
                    self.update_data()
                                
                    if int(time.strftime('%H')) != self.hour:                        
                        self.update_hour(self.hour)
                        self.hour = int(time.strftime('%H'))
                                        
                    if self.hour == 1: # New day 01:00 - clear data
                        self.clear_mqtt_data()                  

                    if time.strftime('%d-%b-%y') != self.sdate: # New day
                        # TODO: clear data (w, lw, etc.)?
                        self.write_file()
                        self.sdate = time.strftime('%d-%b-%y')
                    
                    time.sleep(1)

        except (KeyboardInterrupt, SystemExit, Exception) as e:
            print "Exit...", e
            self.mqtt_client.loop_stop()
            
        
if __name__ == '__main__':
    my_app = PROCESS_ALL()
    my_app.run()
