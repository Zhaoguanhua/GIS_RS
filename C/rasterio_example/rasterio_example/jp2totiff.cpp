#include <iostream>
#include"gdal_priv.h"


int main()
{
	const char *file_path = "D:\\test_data\\T50SQG_20190611T024551_TCI.jp2";
	const char *output_path = "D:\\test_data\\T50SQG_20190611T024551_TCI.tif";

	//��ȡ����
	GDALAllRegister();
	CPLSetConfigOption("GDAL_FILE_IS_UTF8", "NO");

	GDALDataset *input_Ds = (GDALDataset *)GDALOpen(file_path, GA_ReadOnly);

	const char *proj = nullptr;
	double geo[6];

	
	proj = input_Ds->GetProjectionRef();       //ͶӰ��Ϣ
	input_Ds->GetGeoTransform(geo);	           //�������6����
	int Width = input_Ds->GetRasterXSize();    //��
	int Height = input_Ds->GetRasterYSize();   //��
	int bandCount = input_Ds->GetRasterCount();//������

	uint16_t *origin_data = new uint16_t[Width*Height*bandCount];

	input_Ds->RasterIO(GF_Read, 0, 0, Width, Height,
		origin_data, Width, Height, GDT_UInt16, bandCount, 0, 0, 0, 0);


	//�������Ӱ��
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