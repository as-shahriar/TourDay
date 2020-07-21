from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import datetime
# from PIL import Image
# Create your models here.

MONTH_CHOICES = (
    ("Barishal ", "Barishal"),
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

    # slug = models.SlugField(blank=True, null = True, max_length=50)
    date = models.DateField(default=datetime.date.today)
    title = models.CharField(max_length=200, blank=False)
    description =  RichTextUploadingField(max_length = 10000, blank=False)
    image = models.ImageField(upload_to='blog_pics', blank=False)
    division = models.CharField(max_length=20,
                  choices=MONTH_CHOICES,
                  default="Rajshahi")
    

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 1024 or img.width > 1024:
    #         output_size = (400, 580)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    

