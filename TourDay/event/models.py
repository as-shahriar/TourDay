from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    details = models.CharField(max_length=500, null=True, blank=True)
    pay1 = models.CharField(max_length=15, null=True, blank=True)
    pay1_method = models.CharField(max_length=7, null=True, blank=True)
    pay2 = models.CharField(max_length=15, null=True, blank=True)
    pay2_method = models.CharField(max_length=7, null=True, blank=True)
    going = models.ManyToManyField(
        User, related_name="going_user", blank=True)
    pending = models.ManyToManyField(
        User, related_name="pending_user", blank=True)

    def __str__(self):
        return self.title


class Transactions(models.Model):
    event = models.ManyToManyField(Event)
    user = models.ManyToManyField(User)
    tr = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
