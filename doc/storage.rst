Storage
=======

Currently, we expect storage to be managed by parties interested in
publishing imagery to OpenAerialMap. For processed imagery, it is
expected that providers publish appropriately optimized imagery before
indexing it in the OpenAerialMap imagery index. 

.. _optimized:

OpenAerialMap Optimized Image
+++++++++++++++++++++++++++++

In order to make OAM images easy to access for remote clients, the OAM
project is looking to have processed images fulfill a certain set of 
requirements to limit the network traffic needed by OAM tools / intelligent
clients to fetch the data they need where possible.

Generally, what this means is that the image is:

* A Geographic TIFF
* Projected in EPSG:4326
* Has overviews to provide easy access to lower levels of detail
  without reading the entire image.

Processed images will be read by the OpenAerialMap server to gather additional
metadata -- the metadata of the file is presumed to override the metadata
passed in by a user, where available.
