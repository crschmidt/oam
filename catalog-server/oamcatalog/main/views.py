# Create your views here.
from django.http import HttpResponse
import simplejson
from main.models import Layer, Image, User
from main.helpers import *

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
        return json_response(request, i)
    elif id != None:
        i = Image.objects.get(pk=id)
        return json_response(request, i)
    else:
        images = Image.objects.all()
        data = {'images': [
            i.to_json() for i in images 
            ]
        }   
        return json_response(request, data)
