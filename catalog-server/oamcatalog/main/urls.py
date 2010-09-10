from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    # Example:
    (r'^layer/$', 'layer'),
    (r'^layer/$', 'layer'),
    (r'^layer/(?P<id>[0-9]+)/$', 'layer'),
    (r'^image/$', 'image'),
    (r'^image/(?P<id>[0-9]+)/$', 'image'),
)
