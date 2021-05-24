import numpy 
import rasterio
from rasterio.plot import show_hist
import matplotlib.pyplot as plt
from PIL import Image

#CAMBIO EN EL DATATYPE DEL TIF

def TiffToNumpyArrays(OpenedImage):
    imgArrayFloat32 = numpy.array(OpenedImage).astype(numpy.float32)
    imgArrayUINT8 = Image.fromarray(numpy.uint8(imgArrayFloat32*255))
    imgFloat32 = Image.fromarray(numpy.float32(imgArrayUINT8))
   
    imgArray_1 = numpy.array(imgArrayFloat32)
    #convert (para la lista de pixeles que me va a dar la moda, trabaja de 0-255 y luego ya lo devolvemos a 0-1)
    imgArray_255 = numpy.array(imgFloat32)
    #imgArrayUINT8.show()
    return imgArray_1, imgArray_255


def calculateHistogramAndParameters(imagePath):
    OpenedImage = Image.open(imagePath)
    RasterioOpenedImage = rasterio.open(imagePath)
    imgArray_1, imgArray_255 = TiffToNumpyArrays(OpenedImage)
    media=numpy.nanmean(imgArray_1)
    return media

media_ndvi=calculateHistogramAndParameters('/home/pi/Desktop/8-GIT/repos/resources/NDVI_2019_1.tif')


