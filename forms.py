from django import forms
from sound.models import *

__all__ = (
    'SoundmarkForm',
    'MediaForm',
    'CategoryForm',
    'LinkForm',
)

class SoundmarkForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'editor',}), required=False)
    
    class Meta:
        model = Soundmark

class MediaForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'editor',}), required=False)
    
    class Meta:
        model = Media

class CategoryForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'editor',}), required=False)
    
    class Meta:
        model = Category

class LinkForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'editor',}), required=False)
    
    class Meta:
        model = Link