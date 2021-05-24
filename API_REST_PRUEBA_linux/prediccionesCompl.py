#IMPORTS
import requests
import os
import rasterio
import rasterio.features
import rasterio.warp
from datetime import datetime
from pprint import pprint
url0='http://api.openweathermap.org/data/2.5/forecast'

#FUNCION PARA CONSEGUIR LAT/LONG DEL GEOTIFF Y OBTENER DATA
     #La variable de entrada es un tif
def OpenGeoTiffAndGetData (path):
    with rasterio.open(path) as dataset:

        # Read the dataset's valid data mask as a ndarray.
        mask = dataset.dataset_mask()

        # Extract feature shapes and values from the array.
        for geom, val in rasterio.features.shapes(
                mask, transform=dataset.transform):

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geom = rasterio.warp.transform_geom(
                dataset.crs, 'EPSG:4326', geom, precision=6)

            # Print GeoJSON shapes to stdout.
            longitude=(geom['coordinates'][0][0][0])
            latitude=(geom['coordinates'][0][0][1])
            #print('Latitud:', latitude)
            #print('Longitud:', longitude)
    
    querystring0 = {"lat": {latitude}, "lon": {longitude}, "units" : "metric",
               "appid": "b1d4dd23c70a2c7a252d39d4f6fcd29c"}
    res = requests.request("GET", url0, params=querystring0)
    data = res.json()
    return longitude, latitude, data
#COMPROBAR SI EL ELEMENTO RECORRIDO YA ESTÁ EN LA LISTA O NO --> SÍ ESTÁ (TRUE), NO ESTÁ (FALSE)
def IsInTheList(elemento, lista):
    result = False
    for actual in lista.keys():
        if actual == elemento:
            result = True
    return result
#AGRUPAMOS TODOS LOS DATOS POR DÍAS
def SeparateDays(dataInf):
    dataDates = {}
    for element in dataInf['list']:
        #Calculamos la fecha de cada elemento que tenemos
        diaActual = element['dt_txt'].split(' ')[0] #Esto es un texto del tipo YYYY-MM-DD
        #Comprobammos si en nuestro objeto había algún elemento ya guardado con esta fecha.
        if(IsInTheList(diaActual, dataDates)):
            #añado el valor en caso de que ya este creado en la lista dicho elemento
            dataDates[diaActual].append(element)
        
        else:
            #si no esta primero lo creo y luego ya añado el elemento
            dataDates[diaActual] = []
            dataDates[diaActual].append(element)
    return dataDates
#OBTENER LA TEMPERATURA MAXIMA DE CADA DIA
def GetMaxTemp (dataDate, dataInf):
    listaResultado_temp_max={}
    for dia in dataDate:
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #inicializo a 0
        listaResultado_temp_max[valorDelDia] = 0
        maximo=0
        for dataInf in dataDate[dia]:
            if (dataInf['main']['temp_max']> maximo):
                maximo=dataInf['main']['temp_max']
        listaResultado_temp_max[valorDelDia] = maximo
    return listaResultado_temp_max
#OBTENER LA TEMPERATURA MINIMA DE CADA DIA
def GetMinTemp (dataDate, dataInf):
    listaResultado_temp_min={}
    for dia in dataDate:
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #inicializo a 0
        listaResultado_temp_min[valorDelDia] = 0
        minimo=100
        for dataInf in dataDate[dia]:
            if (dataInf['main']['temp_min']< minimo):
                minimo=dataInf['main']['temp_min']
        listaResultado_temp_min[valorDelDia] = minimo
    return listaResultado_temp_min
#OBTENER LA TEMPERATURA MEDIA DE CADA DIA
def GetMediumTemp (dataDate, dataInf):
    #creo una nueva lista que se va a encargar de darnos el valor de la media de la temperatura diaria
    listaResultado_temp_media={}
    #este for lo que hace es estructurar los datos segun los dias
    for dia in dataDate:
        #pprint(dataDates[dia])
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #lo inicializo a cero
        listaResultado_temp_media[valorDelDia] = 0
        #variable que me va a dar el tamaño de la lista de cada dia que sera entre lo que haya que dividir para el array
        cuantos=0
        #este for me da el valor de la suma del parametro que elijamos para después hacer la división entre el número de sumas y obtener la media.
        for dataInf in dataDate[dia]:
            #pprint(data)
            listaResultado_temp_media[valorDelDia] += dataInf['main']['temp']
            cuantos=cuantos+1
        #calculo ed la media
        listaResultado_temp_media[valorDelDia] = listaResultado_temp_media[valorDelDia]/cuantos
    return listaResultado_temp_media
#OBTENER LA PRESION MEDIA DE CADA DIA EN PASCALES
def GetPressure (dataDate, dataInf):
    listaResultado_presion={}
    #este for lo que hace es estructurar los datos segun los dias
    for dia in dataDate:
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #lo inicializo a cero
        listaResultado_presion[valorDelDia] = 0
        #variable que me va a dar el tamaño de la lista de cada dia que sera entre lo que haya que dividir para el array
        cuantos1=0
        #este for me da el valor de la suma del parametro que elijamos para después hacer la división entre el número de sumas y obtener la media.
        for dataInf in dataDate[dia]:
            #pprint(data)
            listaResultado_presion[valorDelDia] += dataInf['main']['pressure']
            cuantos1=cuantos1+1
        #calculo ed la media
        listaResultado_presion[valorDelDia] = listaResultado_presion[valorDelDia]/cuantos1
    return listaResultado_presion
#OBTENER LA VELOCIDAD DEL VIENTO DE CADA DIA
def GetWindSpeed (dataDate, dataInf):
    listaResultado_windspeed={}
    #este for lo que hace es estructurar los datos segun los dias
    for dia in dataDate:
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #lo inicializo a cero
        listaResultado_windspeed[valorDelDia] = 0
        #variable que me va a dar el tamaño de la lista de cada dia que sera entre lo que haya que dividir para el array
        cuantos2=0
        #este for me da el valor de la suma del parametro que elijamos para después hacer la división entre el número de sumas y obtener la media.
        for dataInf in dataDate[dia]:
            #pprint(data)
            listaResultado_windspeed[valorDelDia] += dataInf['wind']['speed']
            cuantos2=cuantos2+1
        #calculo ed la media
        listaResultado_windspeed[valorDelDia] = listaResultado_windspeed[valorDelDia]/cuantos2
    return listaResultado_windspeed
#MOSTRAR LA HUMEDAD RELATIVA DE CADA DIA
def GetHumidity (dataDate, dataInf):
    listaResultado_humidity={}
    #este for lo que hace es estructurar los datos segun los dias
    for dia in dataDate:
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #lo inicializo a cero
        listaResultado_humidity[valorDelDia] = 0
        #variable que me va a dar el tamaño de la lista de cada dia que sera entre lo que haya que dividir para el array
        cuantos3=0
        #este for me da el valor de la suma del parametro que elijamos para después hacer la división entre el número de sumas y obtener la media.
        for dataInf in dataDate[dia]:
            #pprint(data)
            listaResultado_humidity[valorDelDia] += dataInf['main']['humidity']
            cuantos3=cuantos3+1
        #calculo ed la media
        listaResultado_humidity[valorDelDia] = listaResultado_humidity[valorDelDia]/cuantos3
    return listaResultado_humidity
#OBTENER PRECIPITACIONES DE CADA DIA
def GetPrecipitation (dataDate, dataInf, Raining):
    listaResultado_precipitation_today={}
    for dia in dataDate:
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #inicializo a 0
        listaResultado_precipitation_today[valorDelDia] = 0
        
        #variable que me va a dar el tamaño de la lista de cada dia que sera entre lo que haya que dividir para el array
        cuantos5=0
        #este for me da el valor de la suma del parametro que elijamos para después hacer la división entre el número de sumas y obtener la media.
        for dataInf in dataDate[dia]:
            #pprint(data)
            if Raining < 800:
                listaResultado_precipitation_today[valorDelDia] += dataInf['rain'][0]['3h']
                
            else:
                listaResultado_precipitation_today[valorDelDia] += 0
            cuantos5=cuantos5+1
        #calculo ed la media
        listaResultado_precipitation_today[valorDelDia] = listaResultado_precipitation_today[valorDelDia]/cuantos5
    return listaResultado_precipitation_today
#SABER SI EL DIA ES CLARO O CON NUBES
def GetWeather (dataDate, dataInf):
    listaResultado_weather={}
    #este for lo que hace es estructurar los datos segun los dias
    for dia in dataDate:
        #saco el valor de la fecha pero sin la hora, es decir, solo el dia
        valorDelDia = dataDate[dia][0]['dt_txt'].split(' ')[0]
        #lo inicializo a cero
        listaResultado_weather[valorDelDia] = 0
        #variable que me va a dar el tamaño de la lista de cada dia que sera entre lo que haya que dividir para el array
        cuantos4=0
        #este for me da el valor de la suma del parametro que elijamos para después hacer la división entre el número de sumas y obtener la media.
        for dataInf in dataDate[dia]:
            #pprint(data)
            listaResultado_weather[valorDelDia] += dataInf['weather'][0]['id']
            cuantos4=cuantos4+1
        #calculo ed la media
        listaResultado_weather[valorDelDia] = listaResultado_weather[valorDelDia]/cuantos4
    
    return listaResultado_weather
#MOSTRAR LAS TEMPERATURAS MAXIMA, MINIMA,MEDIA Y LA PRESION
def ShowResults (TempMax,TempMin,TempMed,Pressure):
    
    #TEMPERATURAS MINIMAS
    print("Las temperaturas minimas de cada dia son: ")
    for dia in TempMin.keys():
        print(dia, " - ", "{:.2f}".format(TempMin[dia]), "º") #Redondeo a dos decimales

    #TEMPERATURAS MAXIMAS
    print("Las temperaturas maximas de cada dia son: ")
    for dia in TempMax.keys():
        print(dia, " - ", "{:.2f}".format(TempMax[dia]), "º") #Redondeo a dos decimales

    #TEMPERATURA MEDIA
    print("La media de las temperaturas de los días... ")
    for dia in TempMed.keys():
        print(dia, " - ", "{:.2f}".format(TempMed[dia]), "º") #Redondeo a dos decimales

    #PRESION MEDIA
    print("La media de la presion de los días... ")
    for dia in Pressure.keys():
        print(dia, " - ", "{:.2f}".format(Pressure[dia]), "º") #Redondeo a dos decimales
  
#ACCEDER A UN DATO INTRODUCIENDO YO LA FECHA
def getSingleData(date, listOfData):
    result = False
    try:
        result=listOfData[date]
    except:
        print("Error")
    return result
#ACCEDER A UN DATO DESDE UNA POSICION DE LA LISTA
def accesElementInAListFromPosition(position, list): 
    result = False
    resultName = False
    count = 0
    for element in list.keys():
        if count == position:
            try:
                result = list[element]
                resultName = element
                break
            except:
                print("Error")
        count += 1
    return result, resultName

#main code
Longitud, Latitud, Data =OpenGeoTiffAndGetData('/home/pi/Desktop/8-GIT/repos/resources/NDVI_Olivos_MALAGA.tif')
DataDates= SeparateDays(Data)
ListaResultado_Temp_Max= GetMaxTemp(DataDates, Data)
ListaResultado_Temp_Min= GetMinTemp(DataDates, Data)
ListaResultado_Temp_Media= GetMediumTemp(DataDates,Data)
Lista_Resultado_Presion = GetPressure(DataDates, Data)
Lista_Resultado_WindSpeed = GetWindSpeed(DataDates, Data)
Lista_Resultado_Humidity = GetHumidity(DataDates, Data)
Lista_Resultado_Weather = GetWeather(DataDates, Data)

#ShowResults(ListaResultado_Temp_Max,ListaResultado_Temp_Min, Lista_Resultado_Presion, ListaResultado_Temp_Media)

#solicitar posicion del array dependiendo del dia 
#pos = int(input("Sabiendo que puede elegir los 6 próximos dias, indique de qué dia quiere los datos sabiendo que la cuenta empieza en 0 "))
pos=0 #para trabajar con el dia actual en el que nos encontremos
P , dia = accesElementInAListFromPosition(pos,Lista_Resultado_Presion)
Tmax , dia = accesElementInAListFromPosition(pos,ListaResultado_Temp_Max)
T, dia = accesElementInAListFromPosition(pos,ListaResultado_Temp_Media)
Tmin , dia = accesElementInAListFromPosition(pos,ListaResultado_Temp_Min)
U, dia = accesElementInAListFromPosition(pos,Lista_Resultado_WindSpeed)
RH, dia = accesElementInAListFromPosition(pos, Lista_Resultado_Humidity)
Weather, dia =accesElementInAListFromPosition(pos, Lista_Resultado_Weather)
Lista_Resultado_Precipitation=GetPrecipitation(DataDates,Data, Weather)
Precipitation, dia=accesElementInAListFromPosition(pos, Lista_Resultado_Precipitation)

#SACAR EL COEFICIENTE DE AS+BS
def GetAsBs (ClearOrCloudy):
    coef=0
    if ClearOrCloudy < 801:
        coef = 0.25
    elif ClearOrCloudy  >= 801 or ClearOrCloudy <=802:
        coef = 0.5
    else:
        coef=0.75
    return coef
coef=GetAsBs(Weather)

'''
#Resultados
print("PRESION",dia, P)
print("TMAX",dia, Tmax)
print("TMIN",dia, Tmin)
print("TMEDIA",dia, T)
print ("VELOCIDAD VIENTO",dia, U)
print ("HUMEDAD",dia, RH)
print("PRECIPITACIONES", dia, Precipitation)
#print (dia, Weather)
print ("COEFICIENTE as+bs",coef)
#pprint(DataDates)
'''