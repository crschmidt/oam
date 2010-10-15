#!/bin/sh -x

MYPATH=/mnt/geothumper/data/Haiti/digitalglobe/Quickbird/Post-Event/052301115020_01/052301115020_01_P001_PSH
DEST=/storage/data/haiti/processed/dglobe/quickbird-18
mkdir -p $DEST
cd $MYPATH
for i in *.TIF; do
    if [ ! -f $DEST/${i}_warped.tif ]; then
        gdalwarp --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -rc -multi -t_srs EPSG:4326 -of GTiff $i $DEST/${i}_warped.tif
        gdaladdo --config GDAL_CACHEMAX 800 -r average $DEST/${i}_warped.tif 2 4 8 16 32 64
    fi
done   
