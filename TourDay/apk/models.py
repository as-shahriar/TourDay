from django.db import models

class ApkFile(models.Model):
    version = models.CharField(max_length=100,default="v.")
    apk = models.FileField(upload_to='apk_file/')

    def __str__(self):
        return self.version
