from django import forms
from django.core.exceptions import ValidationError
from .models import Posts

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['option', 'author', 'title', 'text', 'category']

