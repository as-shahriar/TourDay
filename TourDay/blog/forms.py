from django.forms import ModelForm
from .models import blogPost

class blogPostForm(ModelForm):
    class Meta:
        model = blogPost
        fields = ['description']