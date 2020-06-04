from django.shortcuts import render


def loginView(request):
    return render(request, "_auth/login.html")
 
def signupView(request):
    return render(request, "_auth/signup.html")

def forgetPasswordView(request):
    return render(request, "_auth/forget_password.html")

def resetPasswordView(request):
    return render(request,'_auth/reset_password.html')