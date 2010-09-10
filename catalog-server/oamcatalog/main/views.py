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
        print id, request.method
        print "hi"
        data = simplejson.loads(request.raw_post_data)
        print "hi"
        i = Image()
        print "hi"
        i.from_json(data)
        print "hi"
        return HttpResponse(simplejson.dumps(i.to_json()))
        print "hi"
    else:
        pass
        #print "lo"
        #i = Image.objects.get(pk=id)
        #return HttpResponse(simplejson.dumps(i.to_json()))
