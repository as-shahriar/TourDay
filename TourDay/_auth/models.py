from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResetCode(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=32)

    def __str__(self):
        return self.user.username

