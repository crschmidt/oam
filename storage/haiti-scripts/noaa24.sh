#!/bin/sh -x

BASE=""
DEST=/storage/data/haiti/processed/noaa/aerial-24
mkdir -p $DEST
chmod 777 $DEST
for i in /storage/data/haiti/source/noaa/20100124/*.tif; do
    OUTPUT=$DEST/`basename $i`
    if [ ! -f $OUTPUT ]; then 
        cp $i $OUTPUT 
        time nice -n 19 ${BASE}gdaladdo -r average --config GDAL_CACHEMAX 800 $OUTPUT 2 4 8 16 32 64 128 256 512;
    fi
done    
