from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    fb = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Check for valid email and also save changed email to User model """
        if self.email != None:
            validate_email(self.email)
            self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs)
