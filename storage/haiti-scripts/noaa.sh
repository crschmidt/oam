#!/bin/sh -x

MYPATH=/mnt/geothumper/data/Haiti/edcftp.cr.usgs.gov/pub/data/disaster/201001_Earthquake_Haiti/data/AERIAL_NOAA
DEST=/storage/data/haiti/processed/noaa/aerial-17-2
mkdir -p $DEST
chmod 777 $DEST
cd $MYPATH
for i in *.tif; do
    if [ ! -f $DEST/${i}_warped.tif ]; then
        gdal_translate --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 $i $DEST/${i}_warped.tif
        gdaladdo --config GDAL_CACHEMAX 800 -r average $DEST/${i}_warped.tif 2 4 8 16 32 64 128
    fi
done   
