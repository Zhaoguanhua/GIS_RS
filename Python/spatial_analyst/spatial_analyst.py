#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : zhaoguanhua
@Email   : zhaogh@hdsxtech.com
@Time    : 2020/3/6 14:11
@File    : Wave_Interpolation.py
@Software: PyCharm
"""

"""
基于站点数据，使用IDW插值生成海浪面数据，基于面数据生成浪高等值线数据。
"""
import os
import sys
import pandas as pd
import gdal
import ogr
import osr
import time

def read_excel(excel_file):
	"""
	读取站点文本文件
	"""
	#sheet = pd.read_excel(excel_file,usecols=[2,12,13])
	sheet = pd.read_csv(excel_file)
	return sheet

def create_real_field(field_name,layer):
	field_geo = ogr.FieldDefn(field_name, ogr.OFTReal)
	field_geo.SetWidth(24)
	field_geo.SetPrecision(3)
	layer.CreateField(field_geo)  # 创建字段

def create_txt_field(field_name,layer):
	field_geo = ogr.FieldDefn(field_name, ogr.OFTString)
	field_geo.SetWidth(24)  # 设置长度
	layer.CreateField(field_geo)  # 创建字段

def write_point(station_data,point_station_file):
	"""
	站点数据写成shapefile文件
	"""

	#gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO") #支持中文路径
	gdal.SetConfigOption("SHAPE_ENCODING","GBK")          #属性字段支持中文

	strDriverName = "ESRI Shapefile"
	oDriver = ogr.GetDriverByName(strDriverName)
	if oDriver ==None:
		print("{driver} 驱动不可用！".format(driver=strDriverName))
		os._exit(0)

	# 创建矢量数据源
	data_source = oDriver.CreateDataSource(point_station_file)

	#指定坐标系
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326)

	# 创建图层
	wave_layer = data_source.CreateLayer("wave", srs, ogr.wkbPoint)

	#设置字段
	create_real_field("WAVEHEIGHT",wave_layer)
	create_txt_field("WAVEDFROM", wave_layer)
	create_real_field("WAVEPERIOD", wave_layer)
	create_real_field("LAT",wave_layer)
	create_real_field("LNG",wave_layer)
	create_txt_field("TIME", wave_layer)
	create_txt_field("SEANAME", wave_layer)
	create_real_field("RISK", wave_layer)
	create_txt_field("CELLSYSID", wave_layer)

	for index,row in station_data.iterrows():
		#print(index,row["WAVEHEIGHT"],row["LAT"],row["LNG"])

		if((row["LNG"]<100 or row["LNG"]>132)):
			continue
		wave_feature = ogr.Feature(wave_layer.GetLayerDefn())
		wave_feature.SetField("WAVEHEIGHT",row["WAVEHEIGHT"])
		wave_feature.SetField("WAVEDFROM", row["WAVEDFROM"])
		wave_feature.SetField("WAVEPERIOD", row["WAVEPERIOD"])
		wave_feature.SetField("LAT", row["LAT"])
		wave_feature.SetField("LNG", row["LNG"])
		wave_feature.SetField("TIME", row["TIME"])
		wave_feature.SetField("SEANAME", row["SEANAME"])
		wave_feature.SetField("RISK", row["RISK"])
		wave_feature.SetField("CELLSYSID", row["CELLSYSID"])

		wkt = "POINT(%f %f)"%(float(row['LNG']),float(row['LAT']))

		point = ogr.CreateGeometryFromWkt(wkt)
		wave_feature.SetGeometry(point)
		wave_layer.CreateFeature(wave_feature)

		feature=None

def idw(output_file,point_station_file):
	"""
	idw空间插值
	:param output_file:插值结果
	:param point_station_file: 矢量站点数据
	:return:
	"""
	opts = gdal.GridOptions(algorithm="invdistnn:power=2.0:smothing=0.0:radius=1.0:max_points=12:min_points=0:nodata=0.0",
							format="GTiff",outputType=gdal.GDT_Float32,zfield="WAVEHEIGHT")
	gdal.Grid(destName=output_file,srcDS=point_station_file,options=opts)

def counter(tiff_file,line_file):
	"""生成等值线
	:param tiff_file:栅格数据
	:param line_file: 等值线结果
	:return:
	"""
	indataset1 = gdal.Open( tiff_file, gdal.GA_ReadOnly)
	in1 = indataset1.GetRasterBand(1)

	#Generate layer to save Contourlines in
	ogr_ds = ogr.GetDriverByName("ESRI Shapefile").CreateDataSource(line_file)
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326)
	contour_shp = ogr_ds.CreateLayer('contour',srs)

	field_defn = ogr.FieldDefn("ID", ogr.OFTInteger)
	contour_shp.CreateField(field_defn)
	field_defn = ogr.FieldDefn("elev", ogr.OFTReal)
	contour_shp.CreateField(field_defn)

	#Generate Contourlines
	gdal.ContourGenerate(in1, 1, 0, [], 0, 0, contour_shp, 0, 1)
	ogr_ds.Destroy()

def clip_file(tiff_file,clip_file):
	"""栅格数据裁剪
	:param tiff_file:原始栅格数据
	:param clip_file: 裁剪后栅格数据
	:return:
	"""
	# opts=gdal.WarpOptions(format="GTiff",
	# 					  cutlineDSName="D:\project\Python\wave_interpolation\sea_clip_5.shp")
	#gdalwarp =os.path.join(script_path,"tools","gdalwarp.exe")
	cutline = os.path.join(script_path,"shp","sea_clip_5.shp")
	dst=gdal.Warp(clip_file,tiff_file,format="GTiff",cutlineDSName=cutline,cutlineLayer="sea_clip_5")

	# clip_cmd = "{gdalwarp} -cutline {cutline} {input} {output} --config GDAL_FILENAME_IS_UTF8 NO".format(gdalwarp=gdalwarp,cutline=cutline,
	# 																   input=tiff_file,output=clip_file)
	# os.system(clip_cmd)

def main(text_file,tiff_file,contour_file):

	dir_path,file_name = os.path.split(tiff_file)
	point_station_file = os.path.join(dir_path,"point_station.shp") #站点矢量文件
	no_clip_tiff_file = os.path.join(dir_path,"wave.tif")

	station_data=read_excel(text_file)

	#文本文件转矢量点文件
	write_point(station_data,point_station_file)

	#插值
	idw(no_clip_tiff_file,point_station_file)

	#裁剪
	clip_file(no_clip_tiff_file,tiff_file)

	os.remove(no_clip_tiff_file)
	#生成等值线
	counter(tiff_file,contour_file)

if __name__ == '__main__':
	script_path=os.path.split(os.path.realpath(__file__))[0]
	wave_station = sys.argv[1]
	wave_interpolation = sys.argv[2]
	contour_file = sys.argv[3]
	inperpolation_NAME = "WAVEHEIGHT"
	start_t = time.time()
	main(wave_station,wave_interpolation,contour_file)
	end_t = time.time()

	print("总时间:{}s".format((end_t-start_t)))
