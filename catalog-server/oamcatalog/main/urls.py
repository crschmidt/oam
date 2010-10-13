from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    # Example:
    (r'^$', 'home'),
    (r'^image/(?P<id>[0-9]+)/$', 'image_browse'),
    (r'^license/(?P<id>[0-9]+)/$', 'license_browse'),
    (r'^api/layer/$', 'layer'),
    (r'^api/layer/(?P<id>[0-9]+)/$', 'layer'),
    (r'^api/license/$', 'license'),
    (r'^api/license/(?P<id>[0-9]+)/$', 'license'),
    (r'^api/image/$', 'image'),
    (r'^api/image/(?P<id>[0-9]+)/$', 'image'),
)
