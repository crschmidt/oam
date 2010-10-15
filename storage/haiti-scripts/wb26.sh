#!/bin/sh -x


MYPATH="/storage/data/haiti/source/worldbank-rit/ortho/haiti-2010-01-26-1/vnir-ortho-scaled/"
DEST="/storage/data/haiti/processed/worldbank/26/${OUT}"
echo $MYPATH
echo $DEST
mkdir -p $DEST
chmod 777 $DEST
cd $MYPATH
for i in *.tif; do
        if [ ! -f $DEST/${i}_warped.tif ] && mkdir $DEST/${i}.lck ; then
            orthoigen  -P /home/crschmidt/pref.txt --disable-elev --hist-auto-minmax --scale-to-8-bit --geo $i $DEST/${i}_warped.tif
            #gdalwarp --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -rc -multi -t_srs EPSG:4326 $i $DEST/${i}_warped.tif
            gdaladdo --config GDAL_CACHEMAX 800 -r average $DEST/${i}_warped.tif 2 4 8 16 32 64 128 256 512
            gdaltindex $DEST/4326.shp $DEST/${i}_warped.tif
            rmdir $DEST/${i}.lck 
        fi
done 
