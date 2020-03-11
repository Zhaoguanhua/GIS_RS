#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : zhaoguanhua
@Email   : zhaogh@hdsxtech.com
@Time    : 2020/3/11 17:21
@File    : gdal_warp_test.py
@Software: PyCharm
"""
import os
import gdal
import ogr
import osr
def clip(input_tif,mask_file,output_file):
	"""
	gdalwarp矢量裁剪栅格
	:param input_tif:
	:param mask_file:
	:param output_file:
	:return:
	"""

	dst=gdal.Warp(output_file,input_tif,format="GTiff",cutlineDSName=mask_file)

	# gdalwarp =""
	# clip_cmd = "{gdalwarp} -cutline {cutline} {input} {output} --config GDAL_FILENAME_IS_UTF8 NO".format(gdalwarp=gdalwarp,cutline=mask_file,
	# 																   input=input_tif,output=output_file)
	# os.system(clip_cmd)


def project(input_tif,output_tif):
	"""
	gdalwarp栅格投影转换
	:param input_tif:
	:param output_tif:
	:return:
	"""
	opt=gdal.WarpOptions(srcSRS="EPSG:4326",dstSRS="EPSG:32651")
	dst = gdal.Warp(output_tif,input_tif,options=opt)


def resample(input_tif,output_tif):
	"""
	gdalwarp栅格数据重采样
	:param input_tif:
	:param output_tif:
	:return:
	"""
	pass

if __name__ == '__main__':
	input_tif=r"D:\项目\深圳海事局\res\idw.tiff"
	input_mask =r"D:\project\Python\wave_interpolation\shp\sea_clip_5.shp"
	output_clip =r"D:\项目\深圳海事局\clip.tif"
	output_project=r"D:\项目\深圳海事局\clip_proj.tif"
	output_resample=r""
	#clip(input_tif,input_mask,output_clip)
	project(input_tif,output_project)
