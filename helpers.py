import urllib, urllib2, simplejson
from django.utils.encoding import smart_str

def get_lat_lng(location):
    
    # http://djangosnippets.org/snippets/293/
    # http://code.google.com/p/gmaps-samples/source/browse/trunk/geocoder/python/SimpleParser.py?r=2476
    # http://stackoverflow.com/questions/2846321/best-and-simple-way-to-handle-json-in-django
    # http://djangosnippets.org/snippets/2399/
    
    location = urllib.quote_plus(smart_str(location))
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % location
    response = urllib2.urlopen(url).read() 
    result = simplejson.loads(response)
    if result['status'] == 'OK':
       lat = str(result['results'][0]['geometry']['location']['lat'])
       lng = str(result['results'][0]['geometry']['location']['lng'])
       return '%s,%s' % (lat, lng)
    else:
        return ''