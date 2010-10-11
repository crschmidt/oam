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
* With internal tiling at 512px x 512px
* Has overviews to provide easy access to lower levels of detail
  without reading the entire image.

Processed images will be read by the OpenAerialMap server to gather additional
metadata -- the metadata of the file is presumed to override the metadata
passed in by a user, where available.

Imagery Availability
++++++++++++++++++++

One of the consistent problems of distributed storage without
replication is that any point of failure becomes a single point of
failure. As a result, OpenAerialMap will begin life in a position where
failure of a single imagery host may create a situation where some
imagery becomes unavailable for a time.

However, overall this effect is less of a problem early on than it might
otherwise be for a couple reasons:

1. Imagery from OAM is not needed to maintain products, in general. In 
   order to produce a product from OAM, the producer will likely need to
   replicate the content in OAM locally, creating a somewhat redundant
   storage of that content for the purposes of that product. For
   example, if someone wishes to make a tiled mosaic available for a
   given area, they will need to download the source data from the
   distributed nodes, and keep them locally; in this way, a failure at
   some other time from a storage host will not affect the functionality
   of the product.
2. By working with high-quality imagery hosts, we hope to be able to
   provide somewhat stable homes for imagery storage, and maintain those
   relationships as a group. 

However, as the project grows, it is expected that this solution will
grow untenable; as such, investigating fault-tolerant distributed
storage options to help prevent this kind of failure will likely be a
goal of the project.
