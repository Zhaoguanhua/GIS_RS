#include <iostream>
#include"gdal_priv.h"


int main()
{
	const char *file_path = "D:\\test_data\\T50SQG_20190611T024551_TCI.jp2";
	const char *output_path = "D:\\test_data\\T50SQG_20190611T024551_TCI.tif";

	//读取数据
	GDALAllRegister();
	CPLSetConfigOption("GDAL_FILE_IS_UTF8", "NO");

	GDALDataset *input_Ds = (GDALDataset *)GDALOpen(file_path, GA_ReadOnly);

	const char *proj = nullptr;
	double geo[6];

	
	proj = input_Ds->GetProjectionRef();       //投影信息
	input_Ds->GetGeoTransform(geo);	           //仿射矩阵6参数
	int Width = input_Ds->GetRasterXSize();    //宽
	int Height = input_Ds->GetRasterYSize();   //高
	int bandCount = input_Ds->GetRasterCount();//波段数

	uint16_t *origin_data = new uint16_t[Width*Height*bandCount];

	input_Ds->RasterIO(GF_Read, 0, 0, Width, Height,
		origin_data, Width, Height, GDT_UInt16, bandCount, 0, 0, 0, 0);


	//创建输出影像
	GDALDataset *output_DS;
	const char *pszFormat = "GTIFF";
	GDALDriver *poDriver;
	poDriver = GetGDALDriverManager()->GetDriverByName(pszFormat);

	if (poDriver == NULL)
	{
		exit(1);
	}
	char **papszOptions = NULL;
	papszOptions = CSLSetNameValue(papszOptions, "COMPRESS", "LZW");
	output_DS = poDriver->Create(output_path, Width, Height, bandCount, GDT_UInt16, papszOptions);
	output_DS->SetGeoTransform(geo);
	output_DS->SetProjection(proj);

	output_DS->RasterIO(GF_Write, 0, 0, Width, Height, origin_data, Width, Height, GDT_UInt16,
		bandCount, 0, 0, 0, 0);

	GDALClose(input_Ds);
	GDALClose(output_DS);

	delete[] origin_data;
}