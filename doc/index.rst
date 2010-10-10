.. OpenAerialMap documentation master file, created by
   sphinx-quickstart on Sun Oct 10 11:15:05 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OpenAerialMap
=============

About The Project
-----------------

OpenAerialMap seeks to act as a steward for the discovery and use of 
open aerial imagery. By bringing together a community of interested 
persons and providing a limited set of tools and expertise around them, 
OpenAerialMap seeks to help solve the problems of persons who need
imagery that is not available through any other means. 

OpenAerialMap is an idea that has been bounced around in many circles for a
long time. The idea of an open source of aerial imagery is one that is not
a new concept, and one that people in the Open Source Geospatial community
have been working around. 

There are many people who have actively expressed interest in the OAM
project, with many different approaches. By taking a simple approach to
the problem, we hope to encourage and allow all of these types of activity
in the OAM community.

The Approach
------------

The OAM 'problem', as it has been described so far, has oftentimes been
bunched with a bunch of other problems. For the purpose of this attmept,
we are going to deliberately and explicitly seperate out the various 
aspects of the problem. 

The key to this approach is to make each step of the process as simple as
possible; that way, there is very little that can't be replicated or replaced
easily, and there are no complex moving parts that require significant 
maintenance. 

The key parts of such an infrastructure are:
  
   * Imagery Index -- a readily accessible way of finding information about
     imagery that is available and how to access it.
   * Storage -- A distributed set of resources through which imagery can be
     made available for access by OAM tools.
   * Access Tools -- Tools which use the Index and access data from Storage
     to build output that users of the OAM data will want. This includes
     everything from a WMS to a set of tiles that can be made available
     offline.

In order to support these mechanisms -- and to keep them seperate -- there
is no association between the Storage and the Index. The OAM project does
not need to provide storage -- instead, we simply document a way for users
to publish their imagery, and document how to list such imagery in a 
publically accessible index.

Imagery Index
+++++++++++++

The imagery index is a list of available imagery. It is designed
to be simple. The primary object that the Catalog focuses on is Images.
An image consists of a URL and some metadata designed to make filtering
and accessing the imagery possible. It will also include a 'cache' of
information determined directly from the imagery that is designed to make
it easier for tools to use the imagery without neccesarily requesting it --
for example, image size in pixels. (This can be combined with the
bounds of the image to generate a resolution, or level of detail, for the
image.)

In addition to acting as an index of images that are prepped for OAM, 
OAM can act as storage for 'archived' images -- image information that is
available, but not processed for access through OAM. (These images 
can then be processed by interested parties and made accessible as 
usable images.)

You'll note that the image objects are associated with a URL. This is
deliberate -- and a big part of the difference between the OAM of the future
and the OAM of the past. Rather than being tied to a single centralized 
server, the OAM catalog is an index of data hosted elsewhere -- allowing that
piece of the puzzle to be easily swapped out for any other.

Storage 
+++++++

In order to make OAM practical, data needs to be stored in a way that it is
easy for tools which are using OAM to access it. What this means, in practice,
is that there is a need to make imagery available from a machine where the
network access is not such that the host of the imagery needs to pay a high
margin on additional requests or bandwidth. 

In the beginning, we expect that many large datasets will not be immediately
available in OAM: instead, we expect that as the imagery is needed, 
organizations will need to find solutions to make their imagery available
in a prepared way for access by OAM consumers. 

Naturally, there are many more imagery providers out there who are able to
provide imagery, but can not provide access to these images in a prepared
form on the web for a number of reasons. We hope to work with these imagery
providers to help them find a home for their imagery that fits their needs --
whether that is solved by joining forces with other organizations like the
Internet Archive, or working with universities to find homes for that data.

One of the primary conditions of the 'storage' layer of OAM is that the 
imagery must be accessible directly, and without significant limit. The 
expectation is that tools which need the imagery can work directly against
it to create products or output. 

At some point, the storage layer of OAM may evolve into access to 
some form of distributed storage; but the underlying means of storing the
data is unimportant to the overall project. Instead, what is important is
that the data can be accessible via a URL. Once you can make data available
from a URL, you can change the underlying mechanism in any way you want.

In order to help move data into the storage layer, part of the OAM project will
be determining the best way to store imagery for ideal access by tools.  For
local disk access, compression oftentimes slows your usage. However, for
network imagery, this is not the case, and as such, a different set of defaults
will need to be built and optimized as the project grows.

The concept behind the storage layer is:
  * Use simple, existing technologies
  * Search out friendly patrons in the short term, and investigate more  
    complete solutions in the long term
  * Treat the URL/HTTP access as the primary way to find information,
    and don't tie storage to any aspect of the catalog directly.

Access Tools
++++++++++++

One of the key problems in the past with OAM has been that with so many
different expectations for it, it has been difficult to reconcile those
expectations in a way that meets a majority of them without overly complicating
the project.

If you think of OpenAerialMap as a URL to access a tiled view of the world, you
will find people who will be unable to use it, because what they really care
about is hyperspectral imagery. If you consider OpenAerialMap to be a source
of imagery used to help generate more accurate reports, you may similarly 
find yourself in competition for resources with people who need access in a
WMS instead of direct access to data.

After careful consideration, it seems that the best approach to this problem
is to take after the OpenStreetMap project: Rather than having all of these
various competing needs be met by the OAM server, concentrate instead on 
creating an index of the imagery of the world which is as complete as possible,
and allow the tools around that to flourish.

OpenStreetMap is an extremely active project for development; in fact,
according to Ohloh, "This is one of the largest open-source teams in the
world, and is in the top 2% of all project teams on Ohloh." This success stems
in large part from encouraging anyone working on code related to the 
OpenStreetMap project to contribute that code directly to the project's SVN,
centralizing developer knowledge and creating an extremely effective shared
community.

The OpenStreetMap.org website is a very small portion of the development
effort: although this is the primary host of the data, everything from
Mapnik-based rendering to many successful editors to tool for analyzing and
mass-updates of the data are maintained in the OpenStreetMap source code
repository.

Our hope with the OAM project is to approach a similar level of transparency
and shared development community by creating a community which is interested
in using the OAM Catalog API and shared understanding of how to make imagery
available, and building tools around it.

In this way, you can imagine someone building a tool which could refer to the
OAM Index and build a tile set for distribution to remote users. You can
imagine someone building a tool which allows a user to simply take a single
snapshot of an area by selecting the imagery that best met their needs. 

At the same time, you could have someone who wrote a tool to download a set of
imagery and put it on a hard drive to ship into a crisis zone, as was done
during the Haiti crisis, to make the source imagery available for deeper
analysis in GIS tools. You can imagine someone building a tool to create a
single, large mosaic -- or make that mosaic avaialble as a WMS.

In all of these cases, we would encourage users to work with the community to
contribute their applications to a centralized home in the OAM project,
centralizing knowledge and effort. 

The key, however, is that this software would then not be maintained directly
by the OAM project in most cases. Other than the Imagery Index, the project
would work to find ways for interested parties to hook up with resources to
host their applications; however, the core of the project would be around
maintaining and improving the imagery index.

Contents:

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

