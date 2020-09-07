from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    detais = models.CharField(max_length=500, null=True, blank=True)
    going = models.ManyToManyField(User)
    pending = models.ManyToManyField(User, related_name="pending_user")

    def __str__(self):
        return self.title


class Transactions(models.Model):
    event = models.ManyToManyField(Event)
    user = models.ManyToManyField(User)
    tr = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username
