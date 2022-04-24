import pandas as pd
import numpy as np
from osgeo import gdal
def precision(tifFile,csvFile):
    gfsi=gdal.Open(tifFile)
    data = pd.read_csv(csvFile)
    ToF = gfsi.GetRasterBand(1).ReadAsArray().astype(np.float32)
    True_data = np.array(data)
    length=len(True_data)
    Tnum=0
    Fnum=0
    for i in range(length):
        if (ToF[True_data[i,0],True_data[i,1]]>=(-0.01) )and True_data[i,2]==True:
            Tnum+=1
        elif (ToF[True_data[i,0],True_data[i,1]]<(-0.01) )and True_data[i,2]==False:
            Tnum+=1
        else:
            Fnum+=1
    prep=(Tnum/(Tnum+Fnum))*100
    return prep
