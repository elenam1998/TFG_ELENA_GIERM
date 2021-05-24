from gpiozero import Button
import time
import math


wind_interval=5
wind_count=0
radius_cm=9.0
ADJUSTMENT=1.18
CM_IN_A_KM=100000
SECS_IN_A_HOUR=3600

def spin():
    global wind_count
    wind_count=wind_count+1

    
def calculate_speed(time_sec):
  
    global wind_count
    circunference_cm=(2*math.pi)*radius_cm
    rotations=wind_count / 2.0

    dist_km =(circunference_cm*rotations)/CM_IN_A_KM

    km_per_sec=dist_km/time_sec
    km_per_hour=km_per_sec*SECS_IN_A_HOUR
    speed=km_per_hour*ADJUSTMENT
    return speed

        
wind_speed_sensor=Button(5)
wind_speed_sensor.when_pressed =spin 

'''
while True:
    wind_count=0
    time.sleep(wind_interval)
    wind_speed=calculate_speed(wind_interval)
    #print(wind_speed, "km/h")

'''
