#!/bin/sh -x

BASE=""

for i in /storage/data/haiti/processed/noaa/aerial-18/*.tif; do
    if ! ${BASE}gdalinfo $i | grep 'Overviews' >/dev/null && mkdir $i.dir; then
        time nice -n 19 ${BASE}gdaladdo -r average --config GDAL_CACHEMAX 800 $i 2 4 8 16 32 64 128 256 512;
        rmdir $i.dir
    fi
done    
