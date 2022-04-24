
import datetime
import time
import cv2 as cv
from matplotlib import pyplot as plt
from osgeo import gdal
import numpy as np
import  os
np.seterr(divide='ignore',invalid='ignore')
FilePath='GF_WFV'
input_shape = r"D:\PythonProject\manasi_Project.shp"
SavePath=r'D:\PythonProject\NDSI_GF_WFV\\'
def opentif(tif):
    data=gdal.Open(tif)
    if data=="None":
        print(tif+"图像无法获取")
    return data

def clip(file):
    f=gdal.Open(file)
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%Y%m%d%H%M%S')
    out='D:\PythonProject\\' + time_str + "_NDSI.tiff",
    ds = gdal.Warp(out,
                   f,
                   format='GTiff',
                   cutlineDSName=input_shape,  # or any other file format
                   cutlineWhere="FIELD = 'whatever'",
                   # optionally you can filter your cutline (shapefile) based on attribute values
                   dstNodata=-9999)  # select the no data value you like
    ds = None  # do other stuff with ds object, it is your cropped dataset. in this case we only close the data
    return out



def ndsi(Blue_tif,Nir_tif):
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y%m%d%H%M%S')
    print(time_str)
    Blue_data = opentif(Blue_tif)
    Nie_data=opentif(Nir_tif)
    cols = Blue_data.RasterXSize
    rows = Blue_data.RasterYSize
    Blue_band = Blue_data.GetRasterBand(1).ReadAsArray(0, 0, cols, rows).astype(np.float32)
    Nir_band = Nie_data.GetRasterBand(4).ReadAsArray(0, 0, cols, rows).astype(np.float32)
    output_ndsi = gdal.GetDriverByName("GTiff")
    file=r'D:\PythonProject\Snow_GF_WFV\\'+time_str+"_GFSI.tiff"
    output_ndsi = output_ndsi.Create(file, cols, rows, bands=1, eType=gdal.GDT_Float32)
    sub=Blue_band-Nir_band
    sum=Blue_band+Nir_band
    ndsi=sub/sum
    im_geotrans = Blue_data.GetGeoTransform()  # 仿射矩阵信息
    im_proj = Blue_data.GetProjection()
    output_ndsi.SetProjection(im_proj)
    output_ndsi.SetGeoTransform(im_geotrans)
    output_ndsi.GetRasterBand(1).SetNoDataValue(65536)
    output_ndsi.GetRasterBand(1).WriteArray(ndsi)

    return file


def ndsi_analyse(file):
    ndsi_data = opentif(file)
    cols = ndsi_data.RasterXSize
    rows = ndsi_data.RasterYSize
    ndsi = ndsi_data.GetRasterBand(1).ReadAsArray(0, 0, cols, rows).astype(np.float32)

    max_ndsi=np.max(ndsi)
    min_ndsi=np.min(ndsi)

    total_num=np.size(ndsi)#总像元值
    nodata_num=np.sum(ndsi==0)#为0的像元值，记作无数据
    havedata_num=total_num-nodata_num#有意义的像元值

    sonw_num=np.sum(ndsi>=-0.01)-nodata_num#大于0.01的像元值为积雪，要减去无意义的值
    pastsonw_num=np.sum(ndsi>=0.02)#大于0.02的为陈雪
    newsnow_num=sonw_num-pastsonw_num#在-0.01~0.02之间的为新雪
    nonesnow_num=total_num-sonw_num-nodata_num#出去雪极为非雪的像元数

    perstage_son=(sonw_num/havedata_num)*100#总体雪的占比例
    perstange_new=(newsnow_num/havedata_num)*100#新雪的占比
    perstange_past=(pastsonw_num/havedata_num)*100#陈雪的占比
    perstange_none=(nonesnow_num/havedata_num)*100#非雪的占比

    ndsi_np=[max_ndsi,min_ndsi,total_num,nodata_num,havedata_num,sonw_num,pastsonw_num,newsnow_num,nonesnow_num]
    ndsi_per=[perstage_son,perstange_new,perstange_past,perstange_none]
    ndsi[ndsi>=-0.01]=1
    ndsi[ndsi<-0.01]=0
    Binary_Image_Path=r'D:\PythonProject\Snow_GF_WFV\Binary_Image.png'
    plt.imsave(Binary_Image_Path, ndsi, cmap='Blues')
    return ndsi_np,ndsi_per,Binary_Image_Path#np数组为像元值以及gfsi的指数  per为积雪的比例























