#!/usr/bin/env python

import sys, os, re, optparse, urllib2
try:
    from hashlib import md5
    md5 # pyflakes
except ImportError:
    import md5
try:
    from osgeo import gdal, gdalconst
    gdal, gdalconst # pyflakes
except ImportError:
    import gdal, gdalconst
try:
    import json
    json # pyflakes
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
    parser.add_option("-u", "--url", dest="url", help="Image URL", default="")
    (opts, args) = parser.parse_args()
    if not opts.service.endswith("/"):
        opts.service += "/"
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
    if re.match(r'\w+://', filename):
        source = "/vsicurl/" + filename # use the VSI curl driver
        url = filename
        filename = url.split("/")[-1]
    else:
        source = filename
        url = None
    dataset = gdal.Open(source, gdalconst.GA_ReadOnly)
    if dataset is None:
        raise Exception("Cannot open %s" % filename)
    xform = dataset.GetGeoTransform()
    bbox = [
       xform[0] + dataset.RasterYSize * xform[2],
       xform[3] + dataset.RasterYSize * xform[5],  
       xform[0] + dataset.RasterXSize * xform[1],
       xform[3] + dataset.RasterXSize * xform[4]
    ]   
    record = {
        "filename": filename,
        "file_format": dataset.GetDriver().ShortName,
        "width": dataset.RasterXSize,
        "height": dataset.RasterYSize,
        "crs": dataset.GetProjection(),
        "file_size": -1,
        "hash": "",
        "bbox": bbox
    }
    if url:
        record["url"] = url
    else:
        record["file_size"] = os.path.getsize(filename)
        record["hash"] = compute_md5(filename)
    return record

def generate_description(filename, opts):
    record = extract_metadata(filename)
    for field in ("user", "url", "layer"):
        record.setdefault(field, getattr(opts, field))
    if not record["url"]:
        raise Exception("URL not specified!")
    if record["url"].endswith("/"):
        record["url"] += os.path.basename(record["filename"])
    return record

def post_description(filename, opts):
    record = generate_description(filename, opts)
    content = json.dumps(record)
    print >>sys.stderr, "Uploading description...",
    req = urllib2.Request(opts.service + "image/")
    try:
        response = urllib2.urlopen(req, content)
    except IOError:
        print >>sys.stderr, "error."
        raise
    result = response.read()
    print >>sys.stderr, "done."
    return json.loads(result)

def walk_path(path, opts):
    pass

def spider(url, opts):
    pass

if __name__ == "__main__":
    opts = parse_options()
    for filename in opts.files:
        if opts.test:
            record = generate_description(filename, opts)
        else:
            record = post_description(filename, opts)
        print json.dumps(record)
