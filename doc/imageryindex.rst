Imagery Index
=============

The imagery index is the core of the OpenAerialMap project. It acts as a
clearinghouse for the OpenAerialMap imagery data.

The core object in the imagery index is an :ref:`image`. There are two types
of images -- an Archive image, and a Processed image. 
 
 * Archive Image: This is designed to be metadata about a file which
   has not been processed for OAM, but which could be processed either by
   tools or by a human. This might mean that the imagery is only available
   in a compressed format, or is in an unusual projection. Generally 
   speaking, this is the case for imagery provided over the web by
   most government agencies.

 * Processed Image: A processed image is an image which has been specifically
   created for OAM, or fits the needs of an OAM client well. For more details,
   see :ref:`optimized`.

The default for images which are uploaded to OpenAerialMap is to be archive
images. To change this, set the archive flag of the image to False when 
uploading.

General API Information
+++++++++++++++++++++++

The Imagery Index API is designed with REST in mind. At its core, each 
resource has a representation as JSON. 

Errors
------

Errors are represented in JSON. They will have an 'error' key, and a 'type'
key. They also have an 'unexpected' key, which indicates whether the 
error is something that application was expecting; in cases where the 
server is broken in some way, you will get an 'unexpected' key set to
true instead of false.

::

  {
    "unexpected": false, 
    "type": "ApplicationError", 
    "error": "No width provided for image., No height provided for image., No BBOX provided for image., No license ID was passed"
  }

.. _image:

Image API
+++++++++

Simplest Image POST::

  {
      "url": "http://example.com/200.tif", 
      "width": 200, 
      "height": 200, 
      "bbox": [-180,-90,180,90], 
      "license": 1
  }

POSTing this to http://catalog.example.com/api/image/ will return a simple 
representation representation::

  { 
    "hash": null,
    "vrt": null,
    "height": 200,
    "bbox": [-180.0, -90.0, 180.0, 90.0],
    "file_size": null,
    "id": 1,
    "crs": null,
    "license": {
      "url":  "",
      "flags": {},
      "name":  "Public Domain",
      "additional":  ""
    },
    "file_format": null,
    "url": "http://example.com/200.tif",
    "vrt_date": null,
    "width": 200
  }
