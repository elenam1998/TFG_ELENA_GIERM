import smbus2
import bme280
import time
import threading

class SENSORBME280(threading.Thread):
    
    def GetTemp (self):
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)
        calibration_params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, calibration_params)
        temp=round(data.temperature,2)
        threading.Timer(5.0, self.GetTemp).start()
        return temp

    def GetHum (self):
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)
        calibration_params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, calibration_params)
        hum=round(data.humidity,2)
        threading.Timer(5.0, self.GetHum).start()
        return hum

    def GetPressure (self):
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)
        calibration_params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, calibration_params)
        pre=round(data.pressure,2)
        threading.Timer(5.0, self.GetPressure).start()
        return pre

data=SENSORBME280()
temp=data.GetTemp()
hum=data.GetHum()
pre=data.GetPressure()
#print(temp,hum,pre)
