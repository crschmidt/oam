#!/usr/bin/env python

try:
    from osgeo import gdal
    gdal # pyflakes
except ImportError:
    import gdal

import sys, array

gdal.SetConfigOption( 'GDAL_TIFF_INTERNAL_MASK', 'YES' )

source = gdal.Open(sys.argv[1], gdal.GA_ReadOnly)
bands = [source.GetRasterBand(i+1) for i in range(source.RasterCount)]

# check that bands 1-3 are RGB
assert [band.GetColorInterpretation() for band in bands] == [gdal.GCI_RedBand, gdal.GCI_GreenBand, gdal.GCI_BlueBand]

target = gdal.GetDriverByName('GTiff').Create( sys.argv[2],
                                          source.RasterXSize,
                                          source.RasterYSize,
                                          3, gdal.GDT_Byte,
                                          [ 'PHOTOMETRIC=YCBCR',
                                            'COMPRESS=JPEG',
                                            'TILED=YES' ] ) 

target_bands = [target.GetRasterBand(i+1) for i in range(3)]
block_width, block_height = target_bands[0].GetBlockSize()

# copy georef
target.SetProjection(source.GetProjection())
target.SetGeoTransform(source.GetGeoTransform())

# Use straight up black if neither alpha nor nodata is present
nodata = [band.GetNoDataValue() for band in bands]
use_alpha = (len(bands) > 4)
use_nodata = (not use_alpha and len([n for n in nodata if n is not None]) == 3)

print >>sys.stderr, "Generating mask from",
if use_alpha:
    print >>sys.stderr, "alpha band."
else:
    if use_nodata:
        print >>sys.stderr, "NODATA values."
        nodata = [chr(int(n)) for n in nodata]
    else:
        print >>sys.stderr, "black pixels."
        nodata = ["\0", "\0", "\0"]
        use_nodata = True

target.CreateMaskBand(gdal.GMF_PER_DATASET)
mask_band = target_bands[0].GetMaskBand()

total_blocks = (target.RasterXSize * target.RasterYSize) / float(block_width * block_height)
blocks_written = 0
sys.stderr.write("0...")

for col in range(0, target.RasterXSize, block_width):
    for row in range(0, target.RasterYSize, block_height):
        width = min(target.RasterXSize - col, block_width)
        height = min(target.RasterYSize - row, block_height)
        data = [band.ReadRaster(col, row, width, height) for band in bands[:3]]
        mask = array.array("B", (1 for x in range(len(data[0]))))
        alpha = None
        if use_alpha:
            alpha = band[3].ReadRaster(col, row, width, height)
        for byte in range(len(data[0])):
            if use_alpha:
                if not alpha[byte]:
                    mask[byte] = 0
            else:
                if data[0][byte] == nodata[0] and data[1][byte] == nodata[1] and data[2][byte] == nodata[2]:
                    mask[byte] = 0
        for n, block in enumerate(data):
            target_bands[n].WriteRaster(col, row, width, height, block)
        mask_band.WriteRaster(col, row, width, height, mask.tostring())
        
        if int(blocks_written / total_blocks * 10) != int((blocks_written + 1) / total_blocks * 10):
            count = int((blocks_written + 1) / total_blocks * 10)
            sys.stderr.write("done." if count == 10 else "%d0..." % count)
        blocks_written += 1

sys.stderr.write("\n")
mask_band = None
target_bands = None
target = None
