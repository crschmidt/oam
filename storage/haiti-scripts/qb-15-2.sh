#!/bin/sh -x
052300482010_01
MYPATH=/mnt/geothumper/data/Haiti/digitalglobe/Quickbird/Post-Event/052300482010_01/052300482010_01_P001_PSH
DEST=/mnt/geodata/haiti/dglobe/quickbird-15
mkdir -p $DEST
chmod 777 $DEST
cd $MYPATH
for i in *.TIF; do
    if [ ! -f $DEST/${i}_warped.tif ]; then
        gdalwarp --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -rc -multi -t_srs EPSG:4326 $i $DEST/${i}_warped.tif
        gdaladdo --config GDAL_CACHEMAX 800 -r average $DEST/${i}_warped.tif 2 4 8 16 32 64
    fi
done   
