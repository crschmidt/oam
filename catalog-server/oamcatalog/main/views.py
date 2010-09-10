# Create your views here.
from django.http import HttpResponse
import simplejson
from main.models import Layer, Image, User

def layer(request, id=None):
    if id == None and request.method == "POST":
        data = simplejson.loads(request.raw_post_data)
        l = Layer()
        l.from_json(data)
        return HttpResponse(simplejson.dumps(l.to_json()))
    elif id != None and id != "all":
        l = Layer.objects.get(pk=id)
        return HttpResponse(simplejson.dumps(l.to_json()))
    else:
        layers = Layer.objects.all()
        data = {'layers': [
            l.to_json() for l in layers
            ]
        }    
        return HttpResponse(simplejson.dumps(data))
            

def image(request, id=None):
    if id == None:
        data = simplejson.loads(request.raw_post_data)
        i = Image()
        i.from_json(data)
        return HttpResponse(simplejson.dumps(i.to_json()))
    else:
        i = Image.objects.get(pk=id)
        return HttpResponse(simplejson.dumps(i.to_json()))
