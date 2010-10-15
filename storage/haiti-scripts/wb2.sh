#!/bin/sh -x


echo "`date` - Start $SCENE_ID $OUT $SAT" >>dg.log  
MYPATH="/storage/data/haiti/source/worldbank-rit/ortho/haiti-2010-01-22-1/vnir-ortho-scaled/"
DEST="/storage/data/haiti/processed/worldbank/21/${OUT}"
echo $MYPATH
echo $DEST
mkdir -p $DEST
chmod 777 $DEST
cd $MYPATH
for i in *.tif; do
        if [ ! -f $DEST/${i}_22_warped.tif ] && mkdir $DEST/${i}_22.lck ; then
            /usr/local/bin/ossim-orthoigen  -P /home/crschmidt/pref.txt --disable-elev --hist-auto-minmax --scale-to-8-bit --geo -w tiff_tiled_band_separate $i $DEST/${i}_22_warped.tif
            #gdalwarp --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -rc -multi -t_srs EPSG:4326 $i $DEST/${i}_warped.tif
            /usr/local/bin/gdaladdo --config GDAL_CACHEMAX 800 -r average $DEST/${i}_22_warped.tif 2 4 8 16 32 64 128
            gdaltindex $DEST/4326.shp $DEST/${i}_22_warped.tif
            rmdir $DEST/${i}_22.lck 
        fi
done 
