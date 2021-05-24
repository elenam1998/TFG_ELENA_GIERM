from sensorbme import SENSORBME280
data=SENSORBME280()
temp=data.GetTemp()
hum=data.GetHum()
pre=data.GetPressure()

SENSOR_BME = [
    {"variable": "humedad", "valor":hum}, 
    {"variable": "temperatura", "valor":temp}, 
    {"variable": "presion", "valor":pre} 
]