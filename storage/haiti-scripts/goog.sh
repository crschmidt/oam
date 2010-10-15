#!/bin/sh -x


MYPATH="/storage/data/haiti/source/google/aerial-21/home/singer-prod/candid/rendering/portau_prince/0121d/rendering"
DEST="/storage/data/haiti/processed/google/21"
mkdir -p $DEST
chmod 777 $DEST
cd $MYPATH
for i in *.jp2; do
    OUT=$DEST/${i}_warped.tif
    if [ ! -f $OUT  ] && mkdir $DEST/${i}.lck ; then
        ~/FWTools-2.0.6/bin_safe/gdal_translate --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 $i $OUT 
        #~/FWTools-2.0.6/bin_safe/gdaladdo --config GDAL_CACHEMAX 800 -r average $OUT 2 4 8 16 32 64 128
       # ~/FWTools-2.0.6/bin_safe/gdaltindex $DEST/4326.shp $OUT 
        rmdir $DEST/${i}.lck 
    fi
done 
