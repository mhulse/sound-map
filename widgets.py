from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.conf import settings

DEFAULT_WIDTH = '75%'
DEFAULT_HEIGHT = '350px'
# 43.834526782236814, -37.265625
DEFAULT_LAT = 44.05
DEFAULT_LNG = -123.09

class LocationWidget(forms.TextInput):
    
    def __init__(self, *args, **kwargs):
        
        self.map_width = kwargs.get('map_width', DEFAULT_WIDTH)
        self.map_height = kwargs.get('map_height', DEFAULT_HEIGHT)
        
        super(LocationWidget, self).__init__(*args, **kwargs)
        
        # self.inner_widget = forms.widgets.HiddenInput()
        self.inner_widget = forms.widgets.TextInput()
    
    def render(self, name, value, *args, **kwargs):
        
        if value is None:
            lat, lng = DEFAULT_LAT, DEFAULT_LNG
        else:
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
            lat, lng = float(a), float(b)
        
        js = '''

<script>
	<!--
		
		(function($) {
			
			$(document).ready(function() {
				
				var gmap_%(name)s = new GmapObject;
				gmap_%(name)s.init('%(name)s', '%(lat)s', '%(lng)s');
				
				$('#button_%(name)s').click(function(e) {
					
					e.preventDefault();
					
					gmap_%(name)s.addy();
					
				});
				
			});
			
		})(django.jQuery);
		
	//-->
</script>

        ''' % dict(name=name, lat=lat, lng=lng)
        html = self.inner_widget.render('%s' % name, '%f,%f' % (lat, lng), dict(id='id_%s' % name))
        html += '''

<div class="gmap">
	<input id="address_%(name)s" class="gmap_address" type="textbox">
	<input id="button_%(name)s" class="gmap_button" type="button" value="Geocode">
	<div class="gmap_wrap" style="width:%(width)s;height:%(height)s;">
		<div id="map_%(name)s" class="gmap_map"></div>
		<div class="crosshair"></div>
	</div>
</div>

        ''' % dict(name=name, width=self.map_width, height=self.map_height)
        
        return mark_safe(js + html)
    
    class Media:
        css = {
            'all': ('sound/gmap.css',)
        }
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
            'sound/gmap.js',
        )