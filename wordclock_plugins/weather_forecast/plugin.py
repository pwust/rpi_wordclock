import os
# import pywapi
# from pyowm import OWM
from pyowm.owm import OWM
import Adafruit_DHT
import time
import wordclock_tools.wordclock_colors as wcc


class plugin:
    """
    A class to display the expected weather for a given location.
    Uses pywapi to retrieve information...
    """

    def __init__(self, config):
        """
        Initializations for the startup of the weather forecast
        """
        # Get plugin name (according to the folder, it is contained in)
        print('entered init of plugin wheather_forecast...')
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Weather forecast"
        self.description = "Displays the current temperature"

        self.location_id = config.get('plugin_' + self.name, 'location_id')
        self.weather_service = config.get('plugin_weather_forecast', 'weather_service')
        self.owm_key = config.get('plugin_weather_forecast', 'api_key')

        try:
            self.pin_temp_sensor = int(config.get('wordclock_interface', 'pin_temp_sensor'))
            self.temp_sensor_registered = True
            print('  Registered temperature sensor at pin ' + str(self.pin_temp_sensor) + '.')
        except:
            print('exception thrown while trying to load sensor module :-(')
            print('  Assumes no temperature sensor to be attached.')
            self.temp_sensor_registered = False

    def run(self, wcd, wci):
        """
        Displaying expected temperature
        """
        # Get current forecast
        if self.weather_service == 'yahoo':
            current_weather_forecast = pywapi.get_weather_from_yahoo(self.location_id)
        elif self.weather_service == 'weather_dot_com':
            current_weather_forecast = pywapi.get_weather_from_weather_com(self.location_id)
        elif self.weather_service == 'openweathermap':
            owm = OWM(self.owm_key)
            owm.config['language'] = 'de'
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(self.location_id)
            w = observation.weather
            current_weather_forecast = []
            print(w.temperature('Celsius'))
            current_weather_forecast['current_conditions']['temperature'] = w.temperature('Celsius')['temp']
            # current_weather_forecast['current_conditions']['temp_max'] = w.temperature('Celsius')['temp_max']
            # current_weather_forecast['current_conditions']['temp_min'] = w.temperature('Celsius')['temp_min']
        else:
            print('Warning: No valid weather_forecast found!')
            return
        outdoor_temp = current_weather_forecast['current_conditions']['temperature']
        if self.temp_sensor_registered:
            try:
                sensor = Adafruit_DHT.AM2302
                pin = self.pin_temp_sensor
                #indoor_temp = str(int(round(am2302_ths.get_temperature(self.pin_temp_sensor))))
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                indoor_temp = str(int(round(temperature)))
                wcd.showText(outdoor_temp + '*', count=1, fps=8)
                wcd.showText(indoor_temp + '*', count=1, fg_color=wcc.GREEN, fps=8)
                wcd.showText(outdoor_temp + '*', count=1, fps=8)
                wcd.showText(indoor_temp + '*', count=1, fg_color=wcc.GREEN, fps=8)
            except:
                print('  Failed to read temperature sensor!')
                wcd.showText(outdoor_temp + '*   ' + outdoor_temp + '*   ' + outdoor_temp + '*', count=1, fps=8)
        else:
            wcd.showText(outdoor_temp + '*   ' + outdoor_temp + '*   ' + outdoor_temp + '*', count=1, fps=8)

        if wci.waitForExit(1.0):
            return
