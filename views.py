from django.views.generic import ListView
from sound.models import *
from django.views.decorators.cache import cache_control

class Index(ListView):
    
    context_object_name = 'data'
    template_name = 'sound/index.html'
    
    def get_queryset(self):
        try:
            sid = Soundmark.objects.latest('sid')
        except Soundmark.DoesNotExist:
            sid = None
        return sid
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context

class KML(ListView):
    
    context_object_name = 'data'
    template_name = 'sound/kml.html'
    
    def get_queryset(self):
        return Soundmark.objects.all().values('title', 'latitude', 'longitude')
    
    def get_context_data(self, **kwargs):
        context = super(KML, self).get_context_data(**kwargs)
        return context