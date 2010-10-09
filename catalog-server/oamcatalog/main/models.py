from django.db import models
from django.contrib.auth.models import User
from main.helpers import ApplicationError

class License(models.Model):
    name = models.CharField(max_length=255)
    noncommercial = models.BooleanField(default=False)
    attribution = models.BooleanField(default=False)
    sharealike = models.BooleanField(default=False)
    additional = models.TextField()
    url = models.CharField(max_length=255, blank=True, null=True)
    flaglist = ['noncommercial', 'attribution', 'sharealike']
    def from_json(self, data):
        errors = []
        for key in ['name', 'url', 'restrictions', 'url']:
            setattr(self, key, data.get(key, ''))
        flags = data.get('options', {})
        for flag,value in flags.items():
            if flag not in self.flaglist:
                errors.append("Flag %s not supported: only supports %s" % (flag, ",".join(self.flaglist)))
            if value == "required": 
                setattr(self, flag, True)
            else:
                errors.append("Only value supported for flags is 'required'")
        if errors:
            raise Exception(errors)
        self.save()
        return self
    def to_json(self):
        flags = {}
        for key in self.flaglist:
            if getattr(self, key) == True:
                flags[key] = 'required'

        return {
            'name': self.name,
            'additional': self.additional,
            'url': self.url,
            'flags': flags
        }    

class Attribution(models.Model):
    attribution = models.TextField()

class Layer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User)
    date = models.DateTimeField(blank=True, null=True)
    attribution = models.ForeignKey(Attribution)
    def from_json(self, data):
        self.name = data['name']
        self.description = data['description']
        self.owner = User.objects.get(pk=data['user'])
        self.save()
        return self

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner.id,
            'attribution': self.attribution.to_json(),
            'images': [i.to_json() for i in self.image_set.all()]
        }    

class Image(models.Model):
    url = models.TextField()
    layer = models.ForeignKey(Layer, blank=True, null=True)
    file_size = models.IntegerField()
    file_format = models.CharField(max_length=255)
    crs = models.CharField(max_length=100)
    bbox = models.CharField(max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()
    hash = models.CharField(max_length=100, blank=True, null=True)
    license = models.ForeignKey(License, blank=True, null=True)
    attribution = models.ForeignKey(Attribution, blank=True, null=True)
    vrt = models.TextField(blank=True, null=True)
    archive = models.BooleanField(default=True)
    def from_json(self, data):
        required_keys = ['url', 'width', 'height']
        optional_keys = ['file_size', 'file_format', 'hash', 'crs', 'vrt', 'archive']
        errors = []
        warnings = []
        for key in required_keys:
            if key in data:
                setattr(self, key, data[key])
            elif getattr(self, key) == None:
                errors.append("No %s provided for image." % key)
        for key in optional_keys:
            if key in data:
                setattr(self, key, data[key])
            else:
                warnings.append("Missing %s in image data. This is a recommended field." % key)
        if 'layer' in data:
            errors.append("No layer handling available at this time. Please upload images without a Layer identifier.")
        if 'bbox' in data:
            self.bbox = ",".join(map(str,data['bbox']))
        else:
            errors.append("No BBOX provided for image.")
        if not 'license' in data:
            errors.append("No license ID was passed")
        elif isinstance(data['license'], int):
            self.license = License.objects.get(pk=data['license'])
        elif isinstance(data['license'], dict):
             l = License()
             l.from_json(data['license'])
             l.save()
             self.license = l
        else:
            errors.append("Some license information is required.")
        if errors:
            raise ApplicationError(errors)
        self.save()
        return self
    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'file_size': self.file_size,
            'file_format': self.file_format,
            'crs': self.crs,
            'bbox': map(float, self.bbox.split(",")),
            'width': self.width,
            'height': self.height,
            'hash': self.hash,
            'license': self.license.to_json(),
            'vrt': self.vrt
        }    
