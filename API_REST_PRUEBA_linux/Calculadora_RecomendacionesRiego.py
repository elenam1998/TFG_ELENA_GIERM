from math import exp
from math import sqrt
import prediccionesCompl
import LongitudDelDia
import RadiacionExtraterrestre
import HorasInsolacion
import media_ndvi
from sensorbme import SENSORBME280
from gpiozero import Button
import time
import math
import anemometer
data=SENSORBME280()
wind_interval=5
time.sleep(wind_interval)

url0='http://api.openweathermap.org/data/2.5/forecast'
url1='http://api.openweathermap.org/data/2.5/weather'
ndvi='/home/pi/Desktop/8-GIT/repos/resources/NDVI_Olivos_MALAGA.tif'

#PARA LAS VARIABLES 
Lon, Lat, Data = prediccionesCompl.OpenGeoTiffAndGetData(ndvi)
DataDates= prediccionesCompl.SeparateDays(Data)
ListaResultado_Temp_Max= prediccionesCompl.GetMaxTemp(DataDates, Data)
ListaResultado_Temp_Min= prediccionesCompl.GetMinTemp(DataDates, Data)
Lista_Resultado_Weather = prediccionesCompl.GetWeather(DataDates, Data)
mediaNDVI=media_ndvi.calculateHistogramAndParameters(ndvi)

#solicitar posicion del array dependiendo del dia 
pos=0
Tmax , dia = prediccionesCompl.accesElementInAListFromPosition(pos,ListaResultado_Temp_Max)
Tmin , dia = prediccionesCompl.accesElementInAListFromPosition(pos,ListaResultado_Temp_Min)
Weather, dia =prediccionesCompl.accesElementInAListFromPosition(pos, Lista_Resultado_Weather)
Lista_Resultado_Precipitation=prediccionesCompl.GetPrecipitation(DataDates,Data,Weather)
Precipitation, dia=prediccionesCompl.accesElementInAListFromPosition(pos, Lista_Resultado_Precipitation)
coef=prediccionesCompl.GetAsBs(Weather)
T=data.GetTemp()
RH=data.GetHum()
P=data.GetPressure()
U=anemometer.calculate_speed(wind_interval)

n=HorasInsolacion.ReadingExcel('/home/pi/Desktop/8-GIT/repos/documentation/22-Insolacion_zonas.xlsx', Lon, Lat)
Ra=RadiacionExtraterrestre.ReadingExcel('/home/pi/Desktop/8-GIT/repos/documentation/19-Ra_zonas.xlsx', Lon, Lat)

Longitud, Latitud, Data =LongitudDelDia.OpenGeoTiffAndGetData(ndvi)
N =LongitudDelDia.GetLongitudeOfTheDay (Data)

#Presion de vapor de saturacion a temperatura T [kPa]
ea=0.611*exp((17.27*T)/(T+237.3))
eamin=0.611*exp((17.27*Tmin)/(Tmin+237.3))
eamax=0.611*exp((17.27*Tmax)/(Tmax+237.3))

#Presion de vapor actual
ed=0.5*eamin*(RH/100)+0.5*eamax*(RH/100)

#Pendiente de la curva de presion de vapor [kPa ºC-1]
Pc=(4098*ea)/((T+237.3)**2)

#Radiacion solar entrante [MJ m^-2 d^-1]
#Para dias cubiertos as --> 0.25, dias claros --> as+bs=0.75
Rs=(float(coef)*(float(n)/float(N)))*float(Ra) 
#Rs=5.8
#Radiacion neta entrante de onda corta [MJ m^-2 d^-1]
Rns=0.77*Rs

#Medida de la radiacion de onda corta durante la insolacion [MJ m^-2 d^-1]
Rso=coef*float(Ra)

#Radiacion neta de onda larga [MJ m^-2 d^-1]
Rnl=(4.903*10**-9)*((pow(Tmax,4) + Tmin**4)/2)*(0.34-(0.14*sqrt(ea)))*(1.35*(Rs/Rso)-0.35)

#Radiacion neta
Rn=Rns-Rnl

#Flujo térmico del suelo [MJ m^-2 d^-1]
G=0

#Calor latente de vaporizacion
landa=2.501-(2.631*10**(-3))*T

#Constante Psicosometrica
gamma=0.00163*(P/landa)

#NECESIDADES DE RIEGO NETAS
Nrn=((0.408*Pc*(Rn-G)+gamma*(900/T)+273*U*(ea-ed))/(Pc+gamma*(1+0.34*U)))*((1.25*(mediaNDVI)+0.1)-((Precipitation)*(1.25*0.7)))
print(Nrn)
