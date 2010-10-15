#!/bin/sh -x


#SCENE_ID=052301419050
#OUT=worldview-18
#SAT=Worldview-2 
if [ ! "$SCENE_ID" ]; then echo "Missing SCENE_ID"; exit; fi
if [ ! "$OUT" ]; then echo "Missing OUT"; exit; fi
if [ ! "$SAT" ]; then echo "Missing Sat"; exit; fi
echo "`date` - Start $SCENE_ID $OUT $SAT" >>dg.log  
MYPATH="/storage/data/haiti/source/digitalglobe/$SAT/${SCENE_ID}_01/${SCENE_ID}_01_P001_PSH"
DEST="/storage/data/haiti/processed/dglobe/${OUT}"
echo $MYPATH
echo $DEST
mkdir -p $DEST
chmod 777 $DEST
cd $MYPATH
for i in *.TIF; do
    if [ ! -f $DEST/${i}_warped.tif ]; then
        gdalwarp --config GDAL_CACHEMAX 800 -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -rc -multi -t_srs EPSG:4326 $i $DEST/${i}_warped.tif
        gdaladdo --config GDAL_CACHEMAX 800 -r average $DEST/${i}_warped.tif 2 4 8 16 32 64 128
    fi
done 
echo "`date` - End $SCENE_ID $OUT $SAT" >>dg.log  
echo "`date` - End $SCENE_ID $OUT $SAT" >>dg.log  
