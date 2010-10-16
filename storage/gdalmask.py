#!/usr/bin/env python

try:
    from osgeo import gdal
    gdal # pyflakes
except ImportError:
    import gdal

import sys

gdal.SetConfigOption( 'GDAL_TIFF_INTERNAL_MASK', 'YES' )

source = gdal.Open(sys.argv[1])
bands = [source.GetRasterBand(i+1) for i in range(source.RasterCount)]
block_width, block_height = bands[0].GetBlockSize()

# check that bands 1-3 are RGB
assert [band.GetColorInterpretation() for band in bands] == [gdal.GCI_RedBand, gdal.GCI_GreenBand, gdal.GCI_BlueBand]

target = gdal.GetDriverByName('GTiff').Create( sys.argv[2],
                                          source.RasterXSize,
                                          source.RasterYSize,
                                          3, gdal.GDT_Byte,
                                          [ #'PHOTOMETRIC=YCBCR',
                                            'COMPRESS=JPEG',
                                            'TILED=YES' ] ) 

target_bands = [target.GetRasterBand(i+1) for i in range(3)]

# copy georef
target.SetProjection(source.GetProjection())
target.SetGeoTransform(source.GetGeoTransform())

# Use straight up black if neither alpha nor nodata is present
nodata = [band.GetNoDataValue() for band in bands]
use_alpha = (len(bands) > 4)
use_nodata = (not use_alpha and len([n for n in nodata if n is not None]) == 3)

if use_alpha:
    print >>sys.stderr, "Using alpha band to generate mask."
else:
    if use_nodata:
        print >>sys.stderr, "Using NODATA values to generate mask."
        nodata = [chr(int(n)) for n in nodata]
    else:
        print >>sys.stderr, "Using black to generate mask."
        nodata = ["\0", "\0", "\0"]
        use_nodata = True

target.CreateMaskBand(gdal.GMF_PER_DATASET)
mask_band = target_bands[0].GetMaskBand()

for col in range(0, source.RasterXSize, block_width):
    for row in range(0, source.RasterYSize, block_height):
        data = [band.ReadRaster(col, row, block_width, block_height) for band in bands[:3]]
        mask = '' # ['\1'] * len(data[0])
        alpha = None
        if use_alpha:
            alpha = band[3].ReadRaster(col, row, block_width, block_height)
        for byte in range(len(data[0])):
            value = '\1'
            if use_alpha:
                if not alpha[byte]:
                    value ='\0' #mask[byte] = '\0'
            else:
                if data[0][byte] == nodata[0] and data[1][byte] == nodata[1] and data[2][byte] == nodata[2]:
                    value = '\0' #mask[byte] = '\0'
            mask += value
        for n, block in enumerate(data):
            target_bands[n].WriteRaster(col, row, block_width, block_height, block)
        #mask = "".join(mask)
        mask_band.WriteRaster(col, row, block_width, block_height, mask)
        sys.stderr.write(".")

sys.stderr.write("\n")
mask_band = None
target_bands = None
target = None
