#include <iostream>
#include"gdal_priv.h"

void read_by_rasterband(const char *input_file)
{
	//读取数据
	GDALAllRegister();
	CPLSetConfigOption("GDAL_FILE_IS_UTF8", "NO");

	GDALDataset *input_Ds = (GDALDataset *)GDALOpen(input_file, GA_ReadOnly);

	int Width = input_Ds->GetRasterXSize();
	int Height = input_Ds->GetRasterYSize();
	const char *proj = nullptr;
	double geo[6];

	proj = input_Ds->GetProjectionRef();
	input_Ds->GetGeoTransform(geo);

	GDALRasterBand *input_band1;
	GDALRasterBand *input_band2;
	GDALRasterBand *input_band3;
	input_band1 = input_Ds->GetRasterBand(1);
	input_band2 = input_Ds->GetRasterBand(2);
	input_band3 = input_Ds->GetRasterBand(3);

	//分块读取数据
	int block_height = 10;
	int block_width = 10;

	int slide_size = 10;

	int i = 0;
	int j = 0;
	int block_nums = block_height*block_width;
	uint8_t *origin_data = new uint8_t[block_nums * 3];
	uint8_t *predict_data = new uint8_t[block_nums];
	input_band1->RasterIO(GF_Read, i*slide_size, j*slide_size, block_width, block_height,
		origin_data, block_width, block_height, GDT_Byte, 0, 0);

	input_band2->RasterIO(GF_Read, i*slide_size, j*slide_size, block_width, block_height,
		origin_data + block_nums, block_width, block_height, GDT_Byte, 0, 0);

	input_band3->RasterIO(GF_Read, i*slide_size, j*slide_size, block_width, block_height,
		origin_data + block_nums * 2, block_width, block_height, GDT_Byte, 0, 0);


	for (int depth = 0; depth < 3; depth++)
	{
		for (int row = 0; row < block_height; row++)
		{
			for (int col = 0; col < block_width; col++)
			{

				std::cout << int(origin_data[depth*block_nums + row * block_height + col]) << " ";

			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}

	delete[]origin_data;
	origin_data = nullptr;
}

void read_by_rasterdataset(const char *input_file)
{
	//读取数据
	GDALAllRegister();
	CPLSetConfigOption("GDAL_FILE_IS_UTF8", "NO");

	GDALDataset *input_Ds = (GDALDataset *)GDALOpen(input_file, GA_ReadOnly);

	int Width = input_Ds->GetRasterXSize();
	int Height = input_Ds->GetRasterYSize();
	const char *proj = nullptr;
	double geo[6];

	proj = input_Ds->GetProjectionRef();
	input_Ds->GetGeoTransform(geo);

	//分块读取数据
	int block_height = 10;
	int block_width = 10;

	int slide_size = 10;

	int i = 0;
	int j = 0;
	int block_nums = block_height*block_width;
	uint8_t *origin_data = new uint8_t[block_nums * 3];
	uint8_t *predict_data = new uint8_t[block_nums];
	input_Ds->RasterIO(GF_Read, i*slide_size, j*slide_size, block_width, block_height,
		origin_data, block_width, block_height, GDT_Byte, 3,0,0,0,0);



	for (int depth = 0; depth < 3; depth++)
	{
		for (int row = 0; row < block_height; row++)
		{
			for (int col = 0; col < block_width; col++)
			{

				std::cout << int(origin_data[depth*block_nums + row * block_height + col]) << " ";

			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}

	delete[]origin_data;
	origin_data = nullptr;
}


int main()
{
	const char *input_file = "D:\\test\\clip_ndvi4_ice_geo_byte2.tif";

	read_by_rasterband(input_file);
	read_by_rasterdataset(input_file);
}