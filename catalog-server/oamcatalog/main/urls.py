from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    # Example:
    (r'^api/layer/$', 'layer'),
    (r'^api/layer/(?P<id>[0-9]+)/$', 'layer'),
    (r'^api/license/$', 'license'),
    (r'^api/license/(?P<id>[0-9]+)/$', 'license'),
    (r'^api/image/$', 'image'),
    (r'^api/image/(?P<id>[0-9]+)/$', 'image'),
)
