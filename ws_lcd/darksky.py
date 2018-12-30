#from geopy.geocoders import Nominatim
from datetime import datetime
import requests

# Nominatim().geocode('katwijk', language='en_US')
# Location((52.19660355, 4.39680477612, 0.0))
# Nominatim().geocode('valkenburg, katwijk', language='en_US')
# Location((52.1700154, 4.42608005921, 0.0))

# https://darksky.net/dev/account
# usr: h.n.nikolov@gmail.com
# psw: weather01

class DarkSky(object):
    def __init__(self):
        self.location  = 'Valkenburg, ZH'
        self.latitude  = '52.1700154'
        self.longitude = '4.42608005921'
        
#        location = Nominatim().geocode('valkenburg, katwijk', language='en_US')
#        self.location  = location.address
#        self.latitude  = str(location.latitude)
#        self.longitude = str(location.longitude)

        self.DARK_SKY_API_KEY = "e90ed0e020c89afde966c557076c9cfa"

        # self.option_list = "exclude=currently,minutely,hourly,alerts&units=si"
        self.option_list = "exclude=minutely,hourly,alerts&units=si"
        self.headers     = {'Accept-Encoding': 'gzip'}
        
        self.search_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.response_json = {}

        # Weather icons
        self.weather_icons_array = {"clear-day": u'\uf00d', "clear-night": u'\uf02e', "rain": u'\uf019', "snow": u'\uf01b', "sleet": u'\uf0b5', 
                                    "wind": u'\uf021', "fog": u'\uf014', "cloudy": u'\uf013', "partly-cloudy-day": u'\uf002', 
                                    "partly-cloudy-night": u'\uf086', "hail": u'\uf015', "thunderstorm": u'\uf01e', "tornado": u'\uf056'}                      

        # 28 icons from f095 to f0b0 (61589 to 61616)
        self.moon_phase_array = [u'\uf095', u'\uf096', u'\uf097', u'\uf098', u'\uf099', u'\uf09a', u'\uf09b',
                                 u'\uf09c', u'\uf09d', u'\uf09e', u'\uf09f', u'\uf0a0', u'\uf0a1', u'\uf0a2',
                                 u'\uf0a3', u'\uf0a4', u'\uf0a5', u'\uf0a6', u'\uf0a7', u'\uf0a8', u'\uf0a9',
                                 u'\uf0aa', u'\uf0ab', u'\uf0ac', u'\uf0ad', u'\uf0ae', u'\uf0af', u'\uf0b0' ]

        self.wind_speed_array = [u'\uf0b7', u'\uf0b8', u'\uf0b9', u'\uf0ba', u'\uf0bb', u'\uf0bc', u'\uf0bd',
                                 u'\uf0be', u'\uf0bf', u'\uf0c0', u'\uf0c1', u'\uf0c2', u'\uf0c3' ]


    def request(self):
        response = requests.get("https://api.darksky.net/forecast/"+self.DARK_SKY_API_KEY+"/"+self.latitude+","+self.longitude+","+self.search_date+"?"+self.option_list, headers=self.headers)    
        self.response_json = response.json()


    def get_icon_weather(self):
        weather = str(self.response_json['currently']['icon']) # str(self.response_json['daily']['data'][0]['icon'])

        if weather in self.weather_icons_array:
            return self.weather_icons_array[weather]
        else:
            return self.weather_icons_array["tornado"]


    def get_icon_moon(self):
        moon_phase = self.response_json['daily']['data'][0]['moonPhase'] * 100

        if moon_phase == 100: return u'\f073' # NOTE This is not a moon phase icon
        idx = int(moon_phase/3.57) # idx out of range if moon_phase == 100
        return self.moon_phase_array[idx]
    
    def get_icon_wind(self):
        # Beaufort Wind Scale
        #  0: <  0.5 m/s (  2 km/h)
        #  1: <  1.5 m/s (  5 km/h)
        #  2: <  3.3 m/s ( 11 km/h)
        #  3: <  5.5 m/s ( 19 km/h)
        #  4: <  7.9 m/s ( 28 km/h)
        #  5: < 10.7 m/s ( 38 km/h)
        #  6: < 13.8 m/s ( 49 km/h)
        #  7: < 17.1 m/s ( 61 km/h)
        #  8: < 20.7 m/s ( 74 km/h)
        #  9: < 24.4 m/s ( 88 km/h)
        # 10: < 28.4 m/s (102 km/h)
        # 11: < 32.6 m/s (117 km/h)
        # 12: > 32.6

        wind_speed = self.response_json['currently']['windSpeed']
        wind_speed_icon = self.wind_speed_array[12] # Default

        if   wind_speed <  0.5: wind_speed_icon = self.wind_speed_array[0]
        elif wind_speed <  1.5: wind_speed_icon = self.wind_speed_array[1]
        elif wind_speed <  3.3: wind_speed_icon = self.wind_speed_array[2]
        elif wind_speed <  5.5: wind_speed_icon = self.wind_speed_array[3]
        elif wind_speed <  7.9: wind_speed_icon = self.wind_speed_array[4]
        elif wind_speed < 10.7: wind_speed_icon = self.wind_speed_array[5]
        elif wind_speed < 13.8: wind_speed_icon = self.wind_speed_array[6]
        elif wind_speed < 17.1: wind_speed_icon = self.wind_speed_array[7]
        elif wind_speed < 20.7: wind_speed_icon = self.wind_speed_array[8]
        elif wind_speed < 24.4: wind_speed_icon = self.wind_speed_array[9]
        elif wind_speed < 28.4: wind_speed_icon = self.wind_speed_array[10]
        elif wind_speed < 32.6: wind_speed_icon = self.wind_speed_array[11]
        else:                   wind_speed_icon = self.wind_speed_array[12]
        
        return wind_speed_icon

    def get_chances_rain(self):
        precip_type = None
        precip_prob_c = 0.0
        precip_prob_d = 0.0
        
        if 'precipProbability' in self.response_json['currently']:
            precip_prob_c = self.response_json['currently']['precipProbability']
        
        if 'precipProbability' in self.response_json['daily']['data'][0]:
            precip_prob_d = self.response_json['daily']['data'][0]['precipProbability']
      
#        return precip_prob_c * 100
        return max(precip_prob_c, precip_prob_d) * 100
        
#        if 'precipType' in self.response_json['currently']:
#            precip_type = self.response_json['currently']['precipType']
#        
#        if precip_type != None and precip_prob != None: # precip_type == 'rain', 'snow', 'sleet'
#            precip_prob *= 100
#            print('Chance of {}: {:.0f}%'.format(precip_type, precip_prob))
    
    def get_location(self):
        return self.location
        
    def get_temperature(self):
        return self.response_json['currently']['temperature']

    def get_apparent_temperature(self):
        return self.response_json['currently']['apparentTemperature']

    def get_apparent_temperature_low(self):
        return self.response_json['daily']['data'][0]['apparentTemperatureLow']

    def get_apparent_temperature_high(self):
        return self.response_json['daily']['data'][0]['apparentTemperatureHigh']

    def get_humidity(self): 
        humidity = self.response_json['currently']['humidity'] # self.response_json['daily']['data'][0]['humidity']
        return humidity * 100
        
    def get_pressure(self): 
        return self.response_json['currently']['pressure']
        

if __name__ == '__main__':
    ds = DarkSky()
    ds.request()
#    print ds.response_json
    print ds.get_location()
    print ds.search_date
#    print str(ds.get_icon_weather())    
#    print str(ds.get_icon_moon())    
#    print ds.get_icon_wind()
    print 'Chances of rain:', ds.get_chances_rain()    
    print 'Temperature:', ds.get_temperature()    
    print 'Apparent Temperature:', ds.get_apparent_temperature()    
    print 'Apparent Temperature Low:', ds.get_apparent_temperature_low()    
    print 'Apparent Temperature High:', ds.get_apparent_temperature_high()    
    print 'Humidity:', ds.get_humidity()    
    print 'Pressure:', ds.get_pressure()    
    
    