from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import validate_email
import re

def loginView(request):
    return render(request, "_auth/login.html")
 
def signupView(request):
    return render(request, "_auth/signup.html")

def forgetPasswordView(request):
    return render(request, "_auth/forget_password.html")

def resetPasswordView(request):
    return render(request,'_auth/reset_password.html')




def ajax_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username!="" and password != "":
            user = authenticate(username=username, password=password)
            if user is None:
                try:
                    obj = User.objects.get(email=username)
                    user = authenticate(username=obj.username, password=password)
                except:
                    return JsonResponse({'status':404})  #user not found
            if user is not None:
                login(request, user)
                return JsonResponse({'status':200})  #user found
        else:
            return JsonResponse({'status':400}) #bad request


def ajax_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username!="" and password != "" and email!="":
                               #TODO: Implement regx check here
            try:
            # if True:
                if re.match(r"^[a-zA-Z0-9_]+$" ,username) == None:
                    raise ValueError
                validate_email(email)
                if User.objects.filter(email=email).count() >= 1:
                    raise ValueError
                user = User()
                user.username = username
                user.set_password(password)
                user.email = email
                user.save()
            except:
                return JsonResponse({'status':400}) #bad request
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status':200})  #user found
        else:
            return JsonResponse({'status':400}) #bad request


def id_logout(request):
    logout(request)
    return redirect("login_page")

def checkusername(request):
     if request.method == "POST":
        username = request.POST.get('username').strip()
        
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'status':200}) #username  exists
        except:
            return JsonResponse({'status':404}) #username not exists
            

def checkemail(request):
     if request.method == "POST":
        email = request.POST.get('email').strip()
        
        try:
            user = User.objects.get(email=email)
            return JsonResponse({'status':200}) #email  exists
        except:
            return JsonResponse({'status':404}) #email not exists