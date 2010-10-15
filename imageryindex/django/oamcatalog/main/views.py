# Create your views here.
from django.http import HttpResponse
import simplejson
from main.models import Layer, Image, User, License
from main.helpers import *
from django.shortcuts import render_to_response

@jsonexception
def layer(request, id=None):
    if id == None and request.method == "POST":
        data = simplejson.loads(request.raw_post_data)
        l = Layer()
        l.from_json(data)
        return json_response(request, l)
    elif id != None and id != "all":
        l = Layer.objects.get(pk=id)
        return json_response(request, l)
    else:
        layers = Layer.objects.all()
        data = {'layers': [
            l.to_json() for l in layers
            ]
        }    
        return json_response(request, data)
            
@jsonexception
def license(request, id=None):
    if id == None and request.method == "POST":
        data = simplejson.loads(request.raw_post_data)
        l = License()
        l.from_json(data)
        return json_response(request, l)
    elif id != None:
        l = License.objects.get(pk=id)
        if request.method == "POST":
            data = simplejson.loads(request.raw_post_data)
            l.from_json(data)
            l.save()
        return json_response(request, l)
    else:
        licenses = License.objects.all()
        data = {'licenses': [
            l.to_json() for l in licenses 
            ]
        }   
        return json_response(request, data)

@jsonexception
def image(request, id=None):
    if id == None and request.method == "POST":
        data = simplejson.loads(request.raw_post_data)
        i = Image()
        i.from_json(data)
        i.save()
        return json_response(request, i)
    elif id != None:
        i = Image.objects.get(pk=id)
        if request.method == "POST":
            data = simplejson.loads(request.raw_post_data)
            i.from_json(data)
            i.save()
        return json_response(request, i)
    else:
        images = Image.objects.all()
        if 'archive' in request.GET and request.GET['archive'].lower() in ("true", "t", "1"):
            images = images.filter(archive=True)
        else:
            images = images.filter(archive=False)
        limited_images = images
        if 'bbox' in request.GET:
            limited_images = []
            left, bottom, right, top = map(float, request.GET['bbox'].split(","))
            for image in images:
                ileft, ibottom, iright, itop = map(float, image.bbox.split(","))
                inbottom = (((ibottom >= bottom) and (ibottom <= top)) or ((bottom >= ibottom) and (bottom <= itop)))
                intop = (((itop >= bottom) and (itop <= top)) or ((top > ibottom) and (top < itop)))
                inleft = (((ileft >= left) and (ileft <= right)) or ((left >= ileft) and (left <= iright)))
                inright = (((iright >= left) and (iright <= right)) or ((right >= iright) and (right <= iright)))
                intersects = ((inbottom or intop) and (inleft or inright))
                if intersects: 
                    limited_images.append(image)
        data = {'images': [
            i.to_json() for i in limited_images
            ]
        }   
        return json_response(request, data)

def home(request):
    images = Image.objects.order_by("-id")[0:10]
    return render_to_response("home.html", {'images': images})

def license_browse(request, id):
    l = License.objects.get(pk=id)
    images = l.image_set.order_by("-id")[0:5]
    return render_to_response("license.html", {'license': l, 'recent_images': images})

def image_browse(request, id):
    i = Image.objects.get(pk=id)
    return render_to_response("image.html", {'image': i})
