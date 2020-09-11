from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.user.username}.{ext}"
    return f"profile_pics/{instance.user.username}/{filename}"


def post_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return f"profile_pics/{instance.user.username}/posts/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    fb = models.CharField(max_length=50, blank=True, null=True)
    insta = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=101, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    picture = models.ImageField(upload_to=user_directory_path,
                                blank=True, default="defaults/user.png")

    def __str__(self):
        return f"{self.id} {self.user.username}"

    def save(self, *args, **kwargs):
        """Check for valid email and also save changed email to User model """
        if self.email != None:
            validate_email(self.email)
            if User.objects.filter(email=self.email).exclude(
                    username=self.user.username).count() != 0:
                raise ValidationError
            self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to=post_image_path,
                              blank=True)
    date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=17, blank=True, null=True)
    likes = models.ManyToManyField(
        User,  blank=True, related_name="liked_user")

    def __str__(self):
        return f"{self.id} {self.user.username}"
