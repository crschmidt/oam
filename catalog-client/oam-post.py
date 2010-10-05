#!/usr/bin/env python

import sys, os, re, optparse, urllib2, urlparse
try:
    from hashlib import md5
    md5 # pyflakes
except ImportError:
    from md5 import md5
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
        help="OAM service base URL", default="http://adhoc.osgeo.osuosl.org:8000/api/")
    #parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Debug mode (dump HTTP errors)")
    parser.add_option("-t", "--test", dest="test", action="store_true", default=False, help="Test mode (don't post to server)")
    parser.add_option("-r", "--recursive", dest="recursive", action="store_true", default=False, help="Perform recursive HTTP/FTP queries.")
    parser.add_option("-c", "--license", dest="license", help="Redistribution license name")
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
    h = md5()
    print >>sys.stderr, ""
    for i in range(0, filesize, blocksize):
        h.update(f.read(blocksize)) 
        print >>sys.stderr, "\rComputing MD5... %d%%" % (float(i)/filesize*100),
    print >>sys.stderr, "\rComputing MD5... done."
    return h.hexdigest()

def extract_metadata(filename):
    print >>sys.stderr, "? %s " % filename.split("/")[-1],
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
        "file_format": dataset.GetDriver().ShortName,
        "width": dataset.RasterXSize,
        "height": dataset.RasterYSize,
        "crs": dataset.GetProjection(),
        "file_size": None,
        "hash": None,
        "bbox": bbox
    }
    if url:
        record["url"] = url
    else:
        record["file_size"] = os.path.getsize(filename)
        record["hash"] = compute_md5(filename)
        record["filename"] = filename
    return record

def generate_description(filename, opts):
    record = extract_metadata(filename)
    for field in ("user", "url", "layer"):
        record.setdefault(field, getattr(opts, field))
    if not record["crs"]:
        raise Exception("CRS unknown!")
    if not record["url"]:
        raise Exception("URL not specified!")
    if record["url"].endswith("/"):
        record["url"] += os.path.basename(record.pop("filename"))
    record["license"] = {"name": opts.license}
    return record

def post_description(filename, opts):
    record = generate_description(filename, opts)
    content = json.dumps(record)
    print >>sys.stderr, "\r>", filename.split("/")[-1]
    req = urllib2.Request(opts.service + "image/")
    try:
        response = urllib2.urlopen(req, content)
    except IOError:
        print >>sys.stderr, "error."
        raise
    result = response.read()
    return json.loads(result)

def walk_path(path, opts):
    pass

href_match = re.compile(r'href="([^\.][^"]+)"', re.IGNORECASE)
img_match = re.compile(r'\.tiff?', re.IGNORECASE)
dir_match = re.compile(r'/$')

def scrape_http(content):
    imgs = []
    dirs = []
    for href in href_match.findall(content):
        if img_match.search(href):
            imgs.append(href)
        elif dir_match.search(href):
            dirs.append(href)
    return dirs, imgs

def scrape_ftp(content):
    imgs = []
    dirs = []
    for line in content.split("\n"):
        fields = line.split()
        perms, size, file = fields[0], fields[4], fields[8:]
        if perms.startswith("d"):
            dirs.append(file[0])
        elif perms.startswith("l") and file[-1:].endswith("/"):
            dirs.append(file[0])
        elif img_match.search(href):
            imgs.append(file[0])
    return dirs, imgs
            
def spider(urls, opts):
    queue = []
    queue.extend(urls)
    while queue:
        item = queue.pop(0)
        print >>sys.stderr, "<", item, 
        req = urllib2.Request(item)
        try:
            response = urllib2.urlopen(req)
        except IOError, e:
            print >>sys.stderr, e
            continue
        result = response.read()
        if item.startswith("http"):
            subdirs, imgs = scrape_http(result)
        else:
            subdirs, imgs = scrape_ftp(result)
        print >>sys.stderr, len(subdirs), ": subdirs /", len(imgs), "images"
        for subdir in subdirs:
            subdir = urlparse.urljoin(item, subdir)
            if not subdir.startswith(item): continue
            queue.append(subdir)
        for img in imgs:
            img = urlparse.urljoin(item, img)
            if not img.startswith(item): continue
            try:
                if opts.test:
                    record = generate_description(img, opts)
                    print json.dumps(record)
                else:
                    record = post_description(img, opts)
            except Exception, e:
                print >>sys.stderr, e

if __name__ == "__main__":
    opts = parse_options()
    if opts.recursive:
        spider(opts.files, opts)
    else:
        for filename in opts.files:
            if opts.test:
                record = generate_description(filename, opts)
            else:
                record = post_description(filename, opts)
            print json.dumps(record)
