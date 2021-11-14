from django.http.response import HttpResponse
from django.shortcuts import render
import numpy as np
from PIL import Image
from osgeo import gdal
from io import BytesIO

def index(request):
    return render(request, 'index.html')


def img(request):
    raster = gdal.Open("static/image/result1.tif")
    band = raster.GetRasterBand(1)
    arr = band.ReadAsArray()
    arr = np.array(arr, dtype=np.float64)
    nodata = band.GetNoDataValue()

    domain = [np.amin(arr[arr != nodata]), np.amax(arr[arr != nodata])]
    number = (arr != nodata)*(0.5 + 255 * arr/domain[1]) + (arr == nodata)*0
    number = np.array(number, dtype=np.int16)

    alpha = (arr != nodata)*255 + (arr == nodata)*0
    _shape = number.shape

    number = number.reshape(_shape[0]*_shape[1],)

    red = bytes((255-number).tolist())
    green = bytes(number.tolist())
    blue = bytes(np.zeros((_shape[0]*_shape[1],), dtype=np.int16).tolist())
    a = bytes(alpha.reshape(_shape[0]*_shape[1],).tolist())

    im_red = Image.frombytes('L', (_shape[1], _shape[0]), red)
    im_green = Image.frombytes('L', (_shape[1], _shape[0]), green)
    im_blue = Image.frombytes('L', (_shape[1], _shape[0]), blue)
    im_alpha = Image.frombytes('L', (_shape[1], _shape[0]), a)


    result = Image.merge('RGBA', (im_red, im_green, im_blue, im_alpha))
    result.save('ff.png')
    buff = BytesIO()
    result.save(buff, format='PNG')
    buff.seek(0)
    return HttpResponse(buff, content_type="image/png")
    
    
