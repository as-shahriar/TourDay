from .models import ApkFile
from django.shortcuts import render,redirect,HttpResponse
import os
from django.conf import settings
def download(request):
    file = ApkFile.objects.all().first()
    fl = open(file.apk.path,'rb')
    response = HttpResponse(fl,content_type='application/vnd.android.package-archive')
    response['Content-Disposition'] = "attachment; filename=%s" % "tourday."+file.version+".apk"
    return response
    return HttpResponse("ghkhj")
