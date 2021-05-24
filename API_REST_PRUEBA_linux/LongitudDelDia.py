#IMPORTS
import requests, os, rasterio, rasterio.features, rasterio.warp
from datetime import datetime
from pprint import pprint
url1='http://api.openweathermap.org/data/2.5/weather'
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
    res = requests.request("GET", url1, params=querystring0)
    data = res.json()
    return longitude, latitude, data
#CONSEGUIR LAS HORAS DE SOL AL DIA
def GetLongitudeOfTheDay (dataInf):
    sunrise= dataInf['sys']['sunrise']
    sunset= dataInf['sys']['sunset']
    timing = sunset-sunrise
    hours= timing/3600
    return hours
#main
Longitud, Latitud, Data =OpenGeoTiffAndGetData('/home/pi/Desktop/8-GIT/repos/resources/NDVI_Olivos_MALAGA.tif')
N =GetLongitudeOfTheDay (Data)
#print("La longitud del dia es de :", N, "horas")