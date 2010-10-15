#!/bin/sh -x

MYPATH=/storage/data/haiti/source/noaa/20100120_NOAA
DEST=/storage/data/haiti/processed/noaa/aerial-20
mkdir -p $DEST
chmod 777 $DEST
cd $MYPATH
for i in *.tif; do
    if [ ! -f $DEST/${i}_warped.tif ]; then
        gdal_translate --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 $i $DEST/${i}_warped.tif
        gdaladdo --config GDAL_CACHEMAX 800 -r average $DEST/${i}_warped.tif 2 4 8 16 32 64 128 256 512 1024
        gdaltindex $DEST/4326.shp $DEST/${i}_warped.tif
    fi
done   
