#!/usr/bin/env python

import sys, os, optparse, urllib2
try:
    from hashlib import md5
except ImportError:
    import md5
try:
    from osgeo import gdal, gdalconst
except ImportError:
    import gdal, gdalconst
try:
    import json
except ImportError:
    import simplejson as json

def parse_options():
    parser = optparse.OptionParser()
    parser.add_option("-U", "--user", dest="user", help="OAM username")
    parser.add_option("-P", "--password", dest="pass", help="OAM password")
    parser.add_option("-s", "--service", dest="service",
        help="OAM service base URL", default="http://adhoc.osgeo.osuosl.org:8000/")
    #parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Debug mode (dump HTTP errors)")
    parser.add_option("-t", "--test", dest="test", action="store_true", default=False, help="Test mode (don't post to server)")
    parser.add_option("-l", "--layer", dest="layer", type="int", help="Layer ID")
    parser.add_option("-u", "--url", dest="url", help="Image URL")
    (opts, args) = parser.parse_args()
    if not opts.service.endswith("/"):
        opts.service += "/"
    for field in ("layer", "url"):
        if not getattr(opts, field):
            setattr(opts, field, args.pop(0))
    opts.files = args
    if len(opts.files) > 1 and not opts.url.endswith("/"):
        raise Exception(
            "URL must end with a / if multiple files are being stored")
    return opts

def compute_md5(filename,blocksize=(1<<20)):
    filesize = os.path.getsize(filename)
    f = file(filename, "rb")
    h = md5.md5()
    for i in range(0, filesize, blocksize):
        h.update(f.read(blocksize)) 
        print >>sys.stderr, "\rComputing MD5... %d%%" % (float(i)/filesize*100),
    print >>sys.stderr, "\rComputing MD5... done."
    return h.hexdigest()

def extract_metadata(filename):
    print >>sys.stderr, "Reading metadata from %s." % filename
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset is None:
        raise Exception("Cannot open %s" % filename)
    xform = dataset.GetGeoTransform()
    bbox = [
       xform[0] + dataset.RasterYSize * xform[2],
       xform[3] + dataset.RasterYSize * xform[5],  
       xform[0] + dataset.RasterXSize * xform[1],
       xform[3] + dataset.RasterXSize * xform[4]
    ]   
    return {
        "filename": filename,
        "file_format": dataset.GetDriver().ShortName,
        "width": dataset.RasterXSize,
        "height": dataset.RasterYSize,
        "crs": dataset.GetProjection(),
        "file_size": os.path.getsize(filename),
        "bbox": bbox,
        "hash": compute_md5(filename)
    }

def generate_description(filename, opts):
    record = extract_metadata(filename)
    for field in ("user", "url", "layer"):
        record.setdefault(field, getattr(opts, field))
    if record["url"].endswith("/"):
        record["url"] += record["filename"]
    return record

def post_description(filename, opts):
    record = generate_description(filename, opts)
    content = json.dumps(record)
    print >>sys.stderr, "Uploading description...",
    req = urllib2.Request(opts.service + "image/")
    try:
        response = urllib2.urlopen(req, content)
    except IOError, e:
        print >>sys.stderr, "error."
        raise
    result = response.read()
    print >>sys.stderr, "done."
    return json.loads(result)

if __name__ == "__main__":
    import pprint
    opts = parse_options()
    for filename in opts.files:
        if opts.test:
            record = generate_description(filename, opts)
        else:
            record = post_description(filename, opts)
        print json.dumps(record)
