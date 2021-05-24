from gpiozero import Button
import time
import math
import anemometer

wind_interval=5
time.sleep(wind_interval)
windspeed=anemometer.calculate_speed(wind_interval)
'''
while True:
    wind_count=0
    time.sleep(wind_interval)
    wind_speed=anemometer.calculate_speed(wind_interval)
'''

WIND_SPEED= [
    {"variable": "Velocidad_Viento", "valor":windspeed}
]

