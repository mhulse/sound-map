import os
from django.contrib import admin
from sound.models import *
from sound.forms import *

#--------------------------------------------------------------------------
#
# Methods:
#
#--------------------------------------------------------------------------

# http://stackoverflow.com/questions/1378447/question-about-admin-py-list-display

def _get_description(obj):
    if obj.description:
        return obj.description
    else:
        return u'(No description)'
_get_description.short_description = u'description'
_get_description.allow_tags = True

def _get_file(obj):
    if obj.file.name:
        return u'<a href="%s">%s</a>' % (obj.file.name, os.path.basename(obj.file.name))
    else:
        return u'(No file)'
_get_file.short_description = u'file'
_get_file.allow_tags = True

# http://www.djangofoo.com/129/format-datetime-in-django-admin
def _get_created(obj):
    return obj.created.strftime('%b %e, %G, %I:%M %p')
_get_created.short_description = 'Created'
_get_created.admin_order_field = 'created'

def _get_modified(obj):
    return obj.modified.strftime('%b %e, %G, %I:%M %p')
_get_modified.short_description = 'Modified'
_get_modified.admin_order_field = 'modified'

#--------------------------------------------------------------------------
#
# Model inlines:
#
#--------------------------------------------------------------------------

class MediaInline(admin.StackedInline):
    
    #----------------------------------
    # Standard options:
    #----------------------------------
    
    fields = ('name', 'photo', 'file', 'uri', 'embed', 'description',)
    form = MediaForm
    
    #----------------------------------
    # Inline-specific options:
    #----------------------------------
    
    model = Media
    extra = 0

#--------------------------------------------------------------------------
#
# Models:
#
#--------------------------------------------------------------------------

class SoundmarkAdmin(admin.ModelAdmin):
    
    #----------------------------------
    # Fields:
    #----------------------------------
    
    prepopulated_fields = {
        'slug': ['title',],
    }
    
    fieldsets = [
        ('Meta', {'fields': ['slug', 'status',], 'classes': ['collapse',],},),
        ('About', {'fields': ['title', 'categories', 'description',],},),
        ('Marker', {'fields': ['address1', 'address2', 'city', 'state', 'zip', 'country', 'geolocation', 'miles',],},),
    ]
    
    exclude = ('phonographer',)
    
    save_on_top = True
    
    #----------------------------------
    # Forms:
    #----------------------------------
    
    form = SoundmarkForm
    
    #----------------------------------
    # Inlines:
    #----------------------------------
    
    inlines = [MediaInline,]
    
    #----------------------------------
    # Change lists:
    #----------------------------------
    
    list_display = ('title', 'status', 'geolocation', _get_description, _get_created, _get_modified,)
    list_display_links = ('title',)
    list_editable = ('status',)
    list_filter = ('status', 'categories',)
    search_fields = ('title', 'description', 'address1', 'address2', 'city', 'state', 'zip', 'country', 'miles',)
    
    #----------------------------------
    # Methods:
    #----------------------------------
    
    def has_change_permission(self, request, obj=None):
        
        has_class_permission = super(SoundmarkAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.phonographer.id:
            return False
        return True
    
    def queryset(self, request):
        
        if request.user.is_superuser:
            return Soundmark.objects.all()
        return Soundmark.objects.filter(phonographer=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.phonographer = request.user
        obj.save()
    
    #----------------------------------
    # Media definitions:
    #----------------------------------
    
    class Media:
        
        css = {
            'all': ('sound/ckeditor.css',)
        }
        js = ('ckeditor/ckeditor.js', 'ckeditor/adapters/jquery.js', 'sound/ckeditor.js',)

class MediaAdmin(admin.ModelAdmin):
    
    #----------------------------------
    # Fields:
    #----------------------------------
    
    fieldsets = [
        ('Meta', {'fields': ['soundmark',], 'classes': ['collapse',],},),
        (None, {'fields': ['name', 'file', 'uri', 'embed', 'description','photo',],},),
    ]
    
    #----------------------------------
    # Forms:
    #----------------------------------
    
    form = MediaForm
    
    #----------------------------------
    # Change lists:
    #----------------------------------
    
    list_display = ('name', _get_file, _get_description, 'soundmark', _get_created, _get_modified,)
    list_display_links = ('name',)
    search_fields = ('name', 'description',)
    
    #----------------------------------
    # Media definitions:
    #----------------------------------
    
    class Media:
        
        css = {
            'all': ('sound/ckeditor.css',)
        }
        js = ('ckeditor/ckeditor.js', 'ckeditor/adapters/jquery.js', 'sound/ckeditor.js',)

class CategoryAdmin(admin.ModelAdmin):
    
    #----------------------------------
    # Fields:
    #----------------------------------
    
    prepopulated_fields = {
        'slug': ['title'],
    }
    
    fieldsets = [
        ('Meta', {'fields': ['slug',], 'classes': ['collapse',],},),
        (None, {'fields': ['parent', 'title', 'description', 'photo',],},),
    ]
    
    #----------------------------------
    # Forms:
    #----------------------------------
    
    form = CategoryForm
    
    #----------------------------------
    # Change lists:
    #----------------------------------
    
    list_display = ('title', 'parent', _get_description,)
    list_display_links = ('title',)
    list_editable = ('parent',)
    search_fields = ('title', 'parent', 'description',)
    
    #----------------------------------
    # Media definitions:
    #----------------------------------
    
    class Media:
        
        css = {
            'all': ('sound/ckeditor.css',)
        }
        js = ('ckeditor/ckeditor.js', 'ckeditor/adapters/jquery.js', 'sound/ckeditor.js',)

class LinkAdmin(admin.ModelAdmin):
    
    #----------------------------------
    # Fields:
    #----------------------------------
    
    prepopulated_fields = {
        'slug': ['title'],
    }
    
    fieldsets = [
        ('Meta', {'fields': ['slug',], 'classes': ['collapse',],},),
        (None, {'fields': ['title', 'uri', 'description', 'photo',],},),
    ]
    
    #----------------------------------
    # Forms:
    #----------------------------------
    
    form = LinkForm
    
    #----------------------------------
    # Change lists:
    #----------------------------------
    
    list_display = ('title', 'uri', _get_description, _get_created, _get_modified,)
    list_display_links = ('title',)
    search_fields = ('title', 'uri', 'description',)
    
    #----------------------------------
    # Media definitions:
    #----------------------------------
    
    class Media:
        
        css = {
            'all': ('sound/ckeditor.css',)
        }
        js = ('ckeditor/ckeditor.js', 'ckeditor/adapters/jquery.js', 'sound/ckeditor.js',)

#--------------------------------------------------------------------------
#
# Registrations:
#
#--------------------------------------------------------------------------

admin.site.register(Soundmark, SoundmarkAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
