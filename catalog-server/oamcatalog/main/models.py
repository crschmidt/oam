from django.db import models
from django.contrib.auth.models import User

class Attribution(models.Model):
    name = models.CharField(max_length=255)
    attribution = models.TextField(blank=True, null=True)
    restrictions = models.TextField()
    def from_json(self, data):
        self.name = data['name']
        self.attribution = data['attribution']
        self.restrictions = data.get('restrictions', '')
        self.save()
        return self
    def to_json(self):
        return {'name': self.name,
            'restrictions': self.restrictions,
            'attribution': self.attribution
        }    

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
        self.attribution = Attribution().from_json(data['attribution'])
        self.save()
        return self

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner.id,
            'attribution': self.attribution.to_json(),
        }    

class Image(models.Model):
    url = models.TextField()
    layer = models.ForeignKey(Layer)
    file_size = models.IntegerField()
    file_format = models.CharField(max_length=255)
    crs = models.CharField(max_length=100)
    bbox = models.CharField(max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()
    def from_json(self, data):
        self.url = data['url']
        self.layer = Layer.objects.get(pk=data['layer'])
        self.file_size = data['file_size']
        self.file_format = data['file_format']
        self.crs = data['crs']
        self.bbox = data['bbox'].join(",")
        self.width = data['width']
        self.height = data['height']
        self.save()
        return self
    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'layer': self.layer.id,
            'file_size': self.file_size,
            'file_format': self.file_format,
            'crs': self.crs,
            'bbox': self.bbox.split(","),
            'width': self.width,
            'height': self.height,
        }    
