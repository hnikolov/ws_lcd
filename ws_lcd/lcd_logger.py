#!/usr/bin/python
import paho.mqtt.client as mqtt
import time, datetime, sys
import traceback

from layout_mix import MY_GUI
from log import LOG

# MQTT_SERVER = "192.168.2.100"
# MQTT_SERVER = "192.168.2.101"
MQTT_SERVER = "localhost"


class MQTT_LOGGER():
    """ Send data via mqtt... """
    def __init__(self, WS = False):
        self.log = LOG(prnt = False, level = 1)

        self.connected = False
        self.dconn     = 0

        self.mqtt_topic_electricity     = "power_meter/electricity"
        self.mqtt_topic_temperature     = "power_meter/temperature"
        self.mqtt_topic_water           = "power_meter/water"
        self.mqtt_topic_gas             = "power_meter/gas"
        self.mqtt_topic_status          = "power_meter/status/A"
        self.mqtt_topic_last_will       = "power_meter/status/L"

        self.mqtt_client = mqtt.Client(client_id="lcd_logger")

        self.mqtt_client.will_set(topic = self.mqtt_topic_last_will, payload="offline", qos=0, retain=True)
        self.mqtt_client.on_connect     = self.on_connect
        self.mqtt_client.on_message     = self.on_message
        self.mqtt_client.on_disconnect  = self.on_disconnect
        self.mqtt_client.on_log         = self.on_log

        self.mqtt_client.disconnect() # Just in case
        self.mqtt_client.connect(MQTT_SERVER, 1883, 60)

        self.my_gui = MY_GUI(WS)

    # MQTT handler ===============================================================================
    def on_log(self, client, userdata, level, buf):
        if "PUBLISH" not in buf:
            self.log.info( buf )

        if "PINGRESP" in buf:
            self.connected = True

    def on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server.
            Subscribing in on_connect() means that if we lose the connection and
            reconnect then subscriptions will be renewed.
        """
#        client.subscribe("power_meter/status/#")
        client.subscribe(self.mqtt_topic_status)
        client.subscribe(self.mqtt_topic_electricity + '/#')
        client.subscribe(self.mqtt_topic_gas + '/#')
        client.subscribe(self.mqtt_topic_water + '/#')
        self.mqtt_client.publish(self.mqtt_topic_last_will, "online, " + str(self.dconn), qos=0, retain=True)
        self.connected = True
        self.log.warning("Connected with result code: " + str(rc))
        self.log.info("Connected to: " + MQTT_SERVER)

    def on_disconnect(self, client, userdata, msg):
        """ The callback for when disconnect from the server. """
        self.log.warning("Disconnected: " + str(msg))
        self.connected = False
        self.dconn    += 1

    def on_message(self, client, userdata, msg):
        """ The callback for when a PUBLISH message is received from the server. """
        st = datetime.datetime.fromtimestamp(msg.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
#        print st[:-3],  ":", msg.topic, ":", msg.payload

        # Note: Update_display from this function does not work
        if msg.topic == self.mqtt_topic_electricity:
            self.my_gui.update_electricity(float(msg.payload)) # kWh

        elif self.mqtt_topic_electricity in msg.topic: # covers /1 /2 ... etc.
            index = int(msg.topic.split('/')[-1])
            self.my_gui.update_electricity_hour(index, float(msg.payload))

        # -----------------------------------------------------------------
        elif msg.topic == self.mqtt_topic_water:
            self.my_gui.update_water(int(msg.payload)) # Litter

        elif self.mqtt_topic_water in msg.topic: 
            index = int(msg.topic.split('/')[-1])
            self.my_gui.update_water_hour(index, int(msg.payload))

        # -----------------------------------------------------------------
        elif msg.topic == self.mqtt_topic_gas:
            self.my_gui.update_gas(float(msg.payload)) # m3, 10 Litters/msg

        elif self.mqtt_topic_gas in msg.topic:
            index = int(msg.topic.split('/')[-1])
            self.my_gui.update_gas_hour(index, float(msg.payload))

#        elif self.mqtt_topic_status == msg.topic:
#            # TODO
#            if "online" in msg.payload:
#                print "A is online"
#            elif "offline" in msg.payload:
#                print "A is offline"
#            print st[:-3],  ":", msg.topic, ":", msg.payload

        self.my_gui.update_eur_total()
    # ===============================================================================

    def connect(self):
        try:
            self.mqtt_client.connect(MQTT_SERVER, 1883, 60)
            self.mqtt_client.loop(timeout = 4.0)
            time.sleep(4) # Do we need this? loop() will timeout after 4s

        except Exception:
            self.log.warning(traceback.format_exc())
            time.sleep(10)

    def display_next(self):
        self.my_gui.layout_next()

    def display_prev(self):
        self.my_gui.layout_prev()

    def display_hour_next(self):
        self.my_gui.hour_data_next()

    def display_hour_prev(self):
        self.my_gui.hour_data_prev()

    # To be removed at some point
    def run_no_buttons(self):
        try:
            self.connect()
            self.mqtt_client.loop_start()

            while True:
                if self.connected == False:
                    self.connect()
                else:
                    self.my_gui.set_date_time()
                    for i in range(5):
                        self.my_gui.update_display() # Updated only when data has changed
                        time.sleep(1)

                    self.my_gui.layout_next()
                    for i in range(5):
                        self.my_gui.update_display() # Updated only when data has changed
                        time.sleep(1)
                    self.my_gui.layout_next()

        except (KeyboardInterrupt, SystemExit):
            self.log.error("Exit...")

        except (Exception) as e:
            self.log.error(traceback.format_exc())

        finally:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self.my_gui.lcd.close()
    # ------------------------------------

    def run(self):
        try:
            while True:
                if self.connected == False:
                    self.connect()

                self.my_gui.set_date_time()
                self.my_gui.update_display() # Updated only when data has changed

                rc = self.mqtt_client.loop()
                if rc != 0:
                    self.log.error("Loop, rc = " + str(rc))

        except (KeyboardInterrupt, SystemExit):
            self.log.error("Exit...")

        except (Exception) as e:
            self.log.error(traceback.format_exc())

        finally:
            self.mqtt_client.disconnect()
            self.my_gui.lcd.close()

# ============================================================================================
if __name__ == '__main__':
    myApp = MQTT_LOGGER(WS=True)
    myApp.run_no_buttons()

