#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : zhaoguanhua
@Email   : zhaogh@hdsxtech.com
@Time    : 2020/6/12 16:46
@File    : read_h5.py
@Software: PyCharm
"""

import gdal
#


#h5格式影像
file = r"D:\COSMO\CSKS1_GEC_B_HI_10_VV_RD_FF_20180115091818_20180115091825.h5"
#输出tiff格式影像
tiff_file =r"D:\test\test.tif"

#获取h5影像的数据集
ds = gdal.Open(file)
subdatasets=ds.GetSubDatasets()
print(subdatasets)

#获取对应的子数据集
dataset = gdal.Open(subdatasets[1][0])

cols = dataset.RasterXSize  #宽
rows = dataset.RasterYSize  #高

#仿射变换矩阵
geos = dataset.GetGeoTransform()
#投影
proj = dataset.GetProjection()
#获取波段
band = dataset.GetRasterBand(1)
#读取数据到内存
data_array = band.ReadAsArray()
print(dataset)
print(geos,proj)

#写入影像
driver = gdal.GetDriverByName("Gtiff")

outdataset = driver.Create(tiff_file, cols, rows, 1, gdal.GDT_Int16)
outdataset.SetGeoTransform(geos)
outdataset.SetProjection(proj)

outband = outdataset.GetRasterBand(1)
outband.WriteArray(data_array)
outband.SetNoDataValue(0)
