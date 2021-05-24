import datetime #, time, math
from influxdb import InfluxDBClient
import Calculadora_RecomendacionesRiego
#import prediccionesCompl, LongitudDelDia, RadiacionExtraterrestre, HorasInsolacion, media_ndvi
#from sensorbme import SENSORBME280
#from gpiozero import Button
#import anemometer

#data=SENSORBME280()
#wind_interval=5
#time.sleep(wind_interval)

# influx configuration 
ifuser = "grafana"
ifpass = "tfg2021"
ifdb   = "tfg"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "DATOS"

# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# format the data as a single measurement for influx
body = [
    {
        "measurement":measurement_name ,
        "time": time,
        "fields": {
            "temperatura actual": Calculadora_RecomendacionesRiego.T ,
            "humedad relativa": Calculadora_RecomendacionesRiego.RH,
            "presion atmosferica": Calculadora_RecomendacionesRiego.P,
            "velocidad del viento": Calculadora_RecomendacionesRiego.U,
            "temperatura maxima": Calculadora_RecomendacionesRiego.Tmax,
            "temperatura minima": Calculadora_RecomendacionesRiego.Tmin,
            "Recomendaciones riego": Calculadora_RecomendacionesRiego.Nrn,  
        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
ifclient.write_points(body)