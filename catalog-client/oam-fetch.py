#!/usr/bin/env python

import sys, os, optparse, urllib2
import urlgrabber, urlgrabber.progress
# try:
#     from osgeo import gdal, gdalconst
# except ImportError:
#     import gdal, gdalconst
try:
    import json
except ImportError:
    import simplejson as json

def parse_options():
    parser = optparse.OptionParser()
    #parser.add_option("-U", "--user", dest="user", help="OAM username")
    #parser.add_option("-P", "--password", dest="pass", help="OAM password")
    parser.add_option("-s", "--service", dest="service",
        help="OAM service base URL", default="http://oam.osgeo.org/api/")
    #parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Debug mode (dump HTTP errors)")
    parser.add_option("-t", "--test", dest="test", action="store_true", default=False, help="Test mode (don't post to server)")
    parser.add_option("-l", "--layer", dest="layer", type="int", help="Layer ID")
    (opts, args) = parser.parse_args()
    if not opts.service.endswith("/"):
        opts.service += "/"
    opts.bbox = map(float, args)
    return opts

def fetch_layer(bbox, opts):
    print >>sys.stderr, "Fetching descriptions...",
    req = urllib2.Request(opts.service + "layer/" + str(opts.layer))
    try:
        response = urllib2.urlopen(req)
    except IOError, e:
        print >>sys.stderr, "error."
        raise
    result = response.read()
    print >>sys.stderr, "done."
    return json.loads(result)

def fetch_images(layer, opts):
    path = str(opts.layer)
    if not opts.test and not os.path.isdir(path):
        os.makedirs(path)
    for image in layer["images"]:
        filetype = image["url"].split(".")[-1]
        target = os.path.join(path, image["hash"] + "." + filetype)
        if opts.test:
            print >>sys.stderr, image["url"], "->", target
        else:
            meter = urlgrabber.progress.text_progress_meter()
            urlgrabber.urlgrab(image["url"], target, progress_obj=meter)

def run_gdalbuildvrt(opts):
    layer_id = str(opts.layer)
    glob = os.path.join(layer_id, "*.*")
    os.system("gdalbuildvrt %s.vrt %s" % (layer_id, glob))

# def merge_bounding_boxes(images):
#     union = list(images[0]["bbox"])
#    for image in images[1:]:
#         bbox = images["bbox"]
#         union = [min(bbox[0], union[0]),
#                  min(bbox[1], union[1]),
#                  max(bbox[2], union[2]),
#                  max(bbox[3], union[3])]
#     return union
# 
# def compute_resolution(image):
#     return (image["bbox"][2] - image["bbox"][0]) / image["width"],
#             image["bbox"][3] - image["bbox"][1]) / image["height"])
# 
# def generate_vrt(layer, opts):
#     bbox = merge_bounding_boxes(layer["images"])
#     xres, yres = compute_resolution(layer["images"][0])
    

if __name__ == "__main__":
    import pprint
    opts = parse_options()
    layer = fetch_layer([], opts)
    fetch_images(layer, opts)
    run_gdalbuildvrt(opts)
