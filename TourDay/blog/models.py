from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class blogPost(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description =  RichTextUploadingField(max_length=10000, blank=True)

