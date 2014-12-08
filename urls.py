from django.conf.urls.defaults import *
from sound.models import *
from sound.views import *

urlpatterns = patterns('',
    
    url(r'^$', Index.as_view(), name='index'),
    url(r'^(?P<snippet_id>[a-zA-Z0-9]{10})\.kml$', KML.as_view(), name='kml'),
#     url(r'^data.kml$', KML.as_view(), name='kml'),
    
)