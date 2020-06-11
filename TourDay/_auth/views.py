from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

def loginView(request):
    return render(request, "_auth/login.html")
 
def signupView(request):
    return render(request, "_auth/signup.html")

def forgetPasswordView(request):
    return render(request, "_auth/forget_password.html")

def resetPasswordView(request):
    return render(request,'_auth/reset_password.html')




def user_login(request):
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