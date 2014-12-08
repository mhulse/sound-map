import datetime
import random
import os.path
from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import *
from django.utils.translation import ugettext_lazy as _
from sound.managers import StatusManager
from sound.fields import LocationField
from sound.functions import get_object_or_None

# https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style

######################################
## 
## For "from <module> import *":
## 
######################################

__all__ = (
    'Soundmark',
    'Media',
    'Category',
    'Link',
)

######################################
## 
## Class methods:
## 
######################################

def _generate_sid(length=10):
    t = 'abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890'
    return ''.join([random.choice(t) for i in range(length)])

######################################
## 
## Abstract models:
## 
######################################

class Base(models.Model):
    
    created  = models.DateTimeField(_(u'Created'), editable=False)
    modified = models.DateTimeField(_(u'Modified'), editable=False)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(Base, self).save(*args, **kwargs)
    
    @property
    def is_modified(self):
        if self.modified > self.created:
            return True
        return False

######################################
## 
## Models:
## 
######################################

class Soundmark(Base):
    
    OPEN_STATUS = 1
    CLOSED_STATUS = 2
    STATUS_CHOICES = (
        (OPEN_STATUS, u'Open'),
        (CLOSED_STATUS, u'Closed'),
    )
    
    sid          = models.CharField(_(u'Secret ID'), max_length=10, editable=False, unique=True, db_index=True)
    status       = models.IntegerField(_(u'status'), choices=STATUS_CHOICES, default=OPEN_STATUS)
    slug         = models.SlugField(_(u'slug'), max_length=255, db_index=True)
    title        = models.CharField(_(u'title'), max_length=255)
    description  = models.TextField(_(u'description'), blank=True)
    address1     = models.CharField(_(u'address'), max_length=255, blank=True)
    address2     = models.CharField(_(u'address (cont.)'), max_length=255, blank=True)
    city         = models.CharField(_(u'city'), max_length=255, blank=True)
    state        = USStateField(_(u'state'), blank=True)
    zip          = models.CharField(_(u'ZIP'), max_length=10, blank=True)
    country      = models.CharField(_(u'country'), max_length=100, blank=True)
    geolocation  = LocationField(_(u'geolocation'), max_length=100)
    longitude    = models.FloatField(_(u'longitude'), editable=False, blank=True)
    latitude     = models.FloatField(_(u'latitude'), editable=False, blank=True)
    miles        = models.DecimalField(_(u'miles'), max_digits=5, decimal_places=2, blank=True, null=True)
    categories   = models.ManyToManyField('Category', blank=True, null=True)
    phonographer = models.ForeignKey(User, blank=True, null=True)
    
    objects = models.Manager() # Admin uses this manager.
    stati = StatusManager()
    
    class Meta:
        unique_together = ('slug', 'longitude', 'latitude')
        ordering = ['-created',]
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def save(self):
        if not self.pk:
            self.sid = _generate_sid()
            # Make sure it's unique:
            while get_object_or_None(Soundmark, sid=self.sid) != None:
                self.sid = _generate_sid()
        if self.geolocation:
            # If geolocation exists, update latitude and longitude fields:
            lat, lon = self.geolocation.split(',')
            self.latitude = float(lat)
            self.longitude = float(lon)
        else:
            # If geolocation does not exist, nuke latitude and longitude fields:
            self.latitude = self.longitude = None
        super(Soundmark, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return('soundmark_detail', (), { 'slug': self.slug })
    
    @property
    def get_geolocation(self):
        if self.geolocation:
            return self.geolocation.split(',')

class Media(Base):
    
    name        = models.CharField(_(u'name'), max_length=255, db_index=True)
    file        = models.FileField(_(u'sound file'), upload_to='sound/media/audio/%Y/%m/%d/', blank=True)
    uri         = models.URLField(_(u'link'), blank=True, help_text='URI to file (this trumps the file field).')
    embed       = models.TextField(_(u'embed html'), blank=True, null=True, help_text='External embed HTML goes here (this trumps the uri and file field).')
    photo       = models.ImageField(_(u'image file'), upload_to='sound/media/photo/%Y/%m/%d/', blank=True, help_text='An image that will be used as a thumbnail.')
    description = models.TextField(_(u'description'), blank=True)
    soundmark   = models.ForeignKey('Soundmark')
    
    class Meta:
        verbose_name = 'media element'
        verbose_name_plural = 'media elements'
        ordering = ['-created',]
    
    def __unicode__(self):
        return u'%s' % self.name

class Category(Base):
    
    # https://github.com/praekelt/django-category/blob/master/category/models.py
    
    slug        = models.SlugField(_(u'slug'), max_length=255, db_index=True, unique=True, help_text='Short descriptive unique name for use in uris.')
    title       = models.CharField(_(u'title'), max_length=200, help_text='Short descriptive name for this category.')
    photo       = models.ImageField(_(u'image file'), upload_to='sound/category/photo/', blank=True, help_text='An image that will be used as a thumbnail.')
    description = models.TextField(_(u'description'), blank=True)
    parent      = models.ForeignKey('self', null=True, blank=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['-title',]
    
    def save(self, *args, **kwargs):
        # Raise on circular reference
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise RuntimeError, 'Circular references not allowed'
            parent = parent.parent
        
        super(Category, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('category_detail', (), { 'slug': self.slug })
    
    def live_soundmark_set(self):
        from sound.models import Soundmark
        return self.soundmark_set.filter(status=Soundmark.LIVE_STATUS)
    
    @property
    def children(self):
        return self.category_set.all().order_by('title')

class Link(Base):
    
    # https://github.com/nathanborror/django-basic-apps/tree/master/basic/bookmarks
    
    slug        = models.SlugField(_('slug'), unique=True)
    title       = models.CharField(_('title'), max_length=100, blank=True, null=True)
    photo       = models.ImageField(_(u'image file'), upload_to='sound/link/photo/', blank=True, help_text='An image that will be used as a thumbnail.')
    uri         = models.URLField(_('uri'), unique=True, help_text='Full URI starting with "http://".')
    description = models.TextField(_('description'), )
    
    class Meta:
        ordering = ['-created',]
    
    def __unicode__(self):
        return self.uri

    def get_absolute_url(self):
        return self.uri