#!/bin/sh -x


MYPATH="/storage/data/haiti/processed/google/21"
cd $MYPATH
for i in *_nearblack.tif; do
    OUT=$i
    if [ ! -f $OUT.done  ] && mkdir ${i}.lck ; then
        gdaladdo -r average --config GDAL_CACHEMAX 800 $OUT 2 4 8 16 32 64 128 256 512
        rmdir ${i}.lck 
        touch $OUT.done
    fi
done 
