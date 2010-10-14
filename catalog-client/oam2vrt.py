import sys, os, optparse, urllib2, StringIO
from xml.etree.ElementTree import ElementTree
try:
    from osgeo import gdal
    gdal
except ImportError:
    import gdal
try:
    import json
    json
except ImportError:
    import simplejson as json

class Image(object):
    __fields__ = ("path", "left", "bottom", "right", "top", "width", "height", "crs", "bands")

    def __init__(self, path, bbox, size, crs=None, vrt=None):
        self.path = path
        self.left, self.bottom, self.right, self.top = bbox
        self.width, self.height = size
        self.crs = crs
        if vrt:
            self.bands = self.get_band_info(vrt)
        assert self.path
        assert self.left < self.right
        assert self.bottom < self.top
        assert self.width > 0
        assert self.height > 0

    @property
    def px_width(self):
        return (self.right - self.left) / float(self.width)

    @property
    def px_height(self):
        return (self.top - self.bottom) / float(self.height)

    @property
    def transform(self):
        return (self.left, self.px_width, 0.0, self.top, 0.0, self.px_height)

    @property
    def bbox(self):
        return (self.left, self.bottom, self.right, self.top)

    def window(self, (left, bottom, right, top)):
        """convert bbox to image pixel window"""
        xoff = int((left - self.left) / self.px_width + 0.0001)
        yoff = int(-(top - self.top) / self.px_height + 0.0001)
        width = int((right - self.left) / self.px_width + 0.5) - xoff
        height = int(-(bottom - self.top) / self.px_height + 0.5) - yoff
        #if width < 1 or height < 1: return ()
        return (xoff, yoff, width, height)

    def intersection(self, (left, bottom, right, top)):
        # figure out intersection region
        left = max(left, self.left)
        right = min(right, self.right)
        top = min(top, self.top)
        bottom = max(bottom, self.bottom)
        # do they even intersect?
        if left >= right or top <= bottom: return ()
        return (left, bottom, right, top)

    def union(self, (left, bottom, right, top)):
        left = min(left, self.left)
        right = max(right, self.right)
        top = max(top, self.top)
        bottom = min(bottom, self.bottom)
        return (left, bottom, right, top)

    def get_band_info(self, vrt):
        if not vrt: return {} 
        bands = {}
        tree = ElementTree()
        tree.parse(StringIO.StringIO(vrt))
        for band in tree.findall("VRTRasterBand"):
            interp = band.find("ColorInterp").text
            props = band.find("SimpleSource/SourceProperties").attrib
            idx = band.find("SimpleSource/SourceBand").text
            bands[interp] = [int(idx), props["DataType"], int(props["BlockXSize"]), int(props["BlockYSize"])]
        return bands

def parse_options():
    parser = optparse.OptionParser()
    #parser.add_option("-U", "--user", dest="user", help="OAM username")
    #parser.add_option("-P", "--password", dest="pass", help="OAM password")
    parser.add_option("-S", "--service", dest="service",
        help="OAM service base URL", default="http://oam.osgeo.org/api/")
    parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Debug mode (dump HTTP errors)")
    #parser.add_option("-t", "--test", dest="test", action="store_true", default=False, help="Test mode (don't post to server)")
    #parser.add_option("-l", "--layer", dest="layer", type="int", help="Layer ID")
    parser.add_option("-a", "--archive", dest="archive", action="store_true", default=False, help="Include archive images")
    parser.add_option("-r", "--resolution", dest="resolution", default="min", help="Resolution strategy (min|max|avg)")
    parser.add_option("-s", "--size", dest="size", help="Output VRT size in pixels (width,height)")
    (opts, args) = parser.parse_args()
    if not opts.service.endswith("/"):
        opts.service += "/"
    opts.output = args.pop(0)
    opts.bbox = map(float, args)
    if len(opts.bbox) != 4 or opts.bbox[0] >= opts.bbox[2] or opts.bbox[1] >= opts.bbox[3]:
        raise Exception("You must provide a proper bounding box!")
    return opts

def call_endpoint(endpoint, opts):
    url = opts.service + endpoint
    if opts.archive:
        if "?" in url:
            url += "&archive=true"
        else:
            url += "?archive=true"
    if opts.debug: print >>sys.stderr, " ", url
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except IOError, e:
        print >>sys.stderr, "error:", e.read()
        raise
    result = response.read()
    return json.loads(result)

def fetch_images(bbox, opts):
    result = call_endpoint("image/?bbox=%f,%f,%f,%f" % tuple(bbox), opts)
    images = []
    for obj in result["images"]:
        image = Image(obj["url"], obj["bbox"], (obj["width"], obj["height"]), obj["crs"], obj["vrt"])
        images.append(image)
    return images

def write_vrt_source(output, target, source, band):
    overlap = source.intersection(target.bbox)
    if not overlap:
        print "ERROR: No overlap between", target.path, "and", source.path
        return
    source_win = source.window(overlap)
    target_win = target.window(overlap)
    if not source_win or not target_win:
        print "ERROR: Source window:", source_win, "Target window:", target_win
        return
    band_idx, data_type, block_width, block_height = source.bands[band]
    output.write('\t\t<ComplexSource>\n')
    output.write(('\t\t\t<SourceFilename relativeToVRT="0">/vsicurl/%s' +
        '</SourceFilename>\n') % source.path)
    output.write('\t\t\t<SourceBand>%i</SourceBand>\n' % band_idx)
    ### TODO: make a config option for this.
    output.write('\t\t\t<NODATA>0</NODATA>\n')
    output.write(('\t\t\t<SourceProperties RasterXSize="%i" RasterYSize="%i"' +
                ' DataType="%s" BlockXSize="%i" BlockYSize="%i"/>\n')
                % (source.width, source.height, data_type, block_width, block_height))
    output.write('\t\t\t<SrcRect xOff="%i" yOff="%i" xSize="%i" ySize="%i"/>\n' % source_win)
    output.write('\t\t\t<DstRect xOff="%i" yOff="%i" xSize="%i" ySize="%i"/>\n' % target_win)
    output.write('\t\t</ComplexSource>\n')

def write_vrt(target, sources):
    """
    if source.px_width != target.px_width or source.px_height != target.px_height:
        print ("All files must have the same scale; %s does not" % source.path)
        sys.exit(1)

    if fi.geotransform[2] != 0 or fi.geotransform[4] != 0:
        print ("No file must be rotated; %s is" % fi.filename)
        sys.exit(1)

    if fi.projection != projection:
        print ("All files must be in the same projection; %s is not" \
            % fi.filename)
        sys.exit(1)
    """
    output = open(target.path, 'w')
    output.write('<VRTDataset rasterXSize="%i" rasterYSize="%i">\n'
        % (target.width, target.height))
    output.write('\t<GeoTransform>%24.16f, %24.16f, %24.16f, %24.16f, %24.16f, %24.16f</GeoTransform>\n'
        % target.transform)

    output.write('\t<SRS>%s</SRS>\n' % target.crs)

    for band, interp in enumerate(('Red', 'Green', 'Blue')):
        output.write('\t<VRTRasterBand dataType="Byte" band="%i">\n' % (band+1))
        output.write('\t\t<ColorInterp>%s</ColorInterp>\n' % interp)
        #output.write('\t\t<NoDataValue>0</NoDataValue>\n')
        for source in sources:
            write_vrt_source(output, target, source, interp)
        output.write('\t</VRTRasterBand>\n')

    output.write('</VRTDataset>\n')

if __name__ == "__main__":
    opts = parse_options()
    images = fetch_images(opts.bbox, opts)
    if not images:
        raise Exception("No images found for that bounding box!")
    # verify that all images have the same SRS
    if len(set(img.crs for img in images)) > 1:
        raise Exception("Not all images have the same CRS!")
    # determine image size based on resolution strategy
    if opts.size:
        width, height = map(int, opts.size.split(","))
    else:
        if opts.resolution == "min":
           target_resolution = min([img.px_width for img in images])
        elif opts.resolution == "max":
           target_resolution = max([img.px_width for img in images])
        else: # avg
           target_resolution = sum([img.px_width for img in images]) / len(images)
        width = int((opts.bbox[2] - opts.bbox[0]) / target_resolution + 0.5)
        height = int((opts.bbox[3] - opts.bbox[1]) / target_resolution + 0.5)
    target = Image(opts.output, opts.bbox, (width, height), images[0].crs) 
    # TODO: do something intelligent about masking/alpha band etc?
    write_vrt(target, images)
