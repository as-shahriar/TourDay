from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import datetime
from PIL import Image


# from sorl.thumbnail import ImageField, get_thumbnail
# Create your models here.

MONTH_CHOICES = (
    ("Barishal", "Barishal"),
    ("Chittagong", "Chittagong"),
    ("Dhaka", "Dhaka"),
    ("Mymensingh", "Mymensingh"),
    ("Khulna", "Khulna"),
    ("Rajshahi", "Rajshahi"),
    ("Rangpur", "Rangpur"),
    ("Sylhet", "Sylhet"),
)

class blogPost(models.Model):
    blog_user = models.ForeignKey(User, on_delete=models.CASCADE)

    slug = models.SlugField(blank=True, null = True, max_length=50)
    date = models.DateField(default=datetime.date.today)
    title = models.CharField(max_length=100, blank=False)
    description =  RichTextUploadingField(blank=False, null=False)
    image = models.ImageField(upload_to='blog_pics', blank=False)
    division = models.CharField(max_length=20,
                  choices=MONTH_CHOICES,
                  default="Rajshahi")
    
    
    

    # def save(self):
    #     super().save()  # saving image first

    #     img = Image.open(self.image.path) # Open image using self

    #     if img.width > 750:
    #         new_img = (750, 450)
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)

    

