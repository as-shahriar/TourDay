from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
# Models
from django.contrib.auth.models import User
from _auth.models import ResetCode

from django.core.validators import validate_email
import re

# delete this
from django.core.mail import send_mail
from utils import async_send_mail
from TourDay.settings import EMAIL_HOST_USER
from django.db.models import Q
from _auth.utils import get_code, get_hash


def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username != "" and password != "":
            user = authenticate(username=username, password=password)
            if user is None:
                try:
                    obj = User.objects.get(email=username)
                    user = authenticate(
                        username=obj.username, password=password)
                except:
                    return JsonResponse({'status': 404})  # user not found
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 200})  # user found
        else:
            return JsonResponse({'status': 400})  # bad request
    return render(request, "_auth/login.html")


def signupView(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username != "" and password != "" and email != "":

            try:
                # if True:
                if re.match(r"^[a-zA-Z0-9_]+$", username) == None:
                    raise ValueError
                validate_email(email)
                if User.objects.filter(email=email).count() >= 1:
                    raise ValueError
                user = User()
                user.username = username
                user.set_password(password)
                user.email = email
                user.save()
                subject = "Welcome to TourDay!"
                message = f"Dear {username},\nYour new TourDay account has been created. Welcome to TourDay Community!\nFrom now on, please log in to your account using your email address or your username and your password.\n\nComplete your account at https://somesamapleaccount.com\n\nIf you received this email but didn't register for an TourDay account, something's gone wrong, Reply to this email to de-activate and close this account.\n\nThanks for registering!\nTourDay Team"
                async_send_mail(subject, message, EMAIL_HOST_USER, email)
            except:
                return JsonResponse({'status': 400})  # bad request

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 200})  # user found
        else:
            return JsonResponse({'status': 400})  # bad request
    return render(request, "_auth/signup.html")


def forgetPasswordView(request):
    if request.method == "POST":
        username_email = request.POST.get('username_email')
        try:
            user = User.objects.get(
                Q(username=username_email) | Q(email=username_email)
            )
            if ResetCode.objects.filter(user=user).count() != 0:
                code_obj = ResetCode.objects.get(user=user)
            else:
                code_obj = ResetCode()
            code_obj.user = user
            code = get_code()
            code_obj.code = get_hash(code)
            code_obj.save()
            subject = "Reset Password | TourDay"
            message = f"Hi {user.username},\nYou recently requested to reset your password for your TourDay account.\n\nCODE: {code}\n\nGoto https://localhost:8000/reset-password/{user.username} and use this code to reset your password.\n\nIf you didn't request a password reset, please ignore this email.\n\nThanks,\nTourDay Team"
            async_send_mail(subject, message, EMAIL_HOST_USER, user.email)

            return JsonResponse({
                "status": 200,
                "slug": user.username
            })
        except:
            return JsonResponse({
                "status": 404,
            })
    return render(request, "_auth/forget_password.html")


def resetPasswordView(request, slug):
    try:
        user = User.objects.get(username=slug)
    except:
        return HttpResponse("404 Not Found")

    if request.method == "POST":
        code = request.POST.get('code')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if code != "" and password1 != "" and password1 == password2 and len(password1) > 7:
            try:
                user = User.objects.get(username=username)
                code_obj = ResetCode.objects.get(user=user)
                if get_hash(code) == code_obj.code:
                    user.set_password(password1)
                    user.save()
                    code_obj.delete()
                    subject = "Success! Password Changed | TourDay"
                    message = f"Hi {user.username},\nSuccess! Your Password has been changed!\n\nIf you didn't changed your password, then your account is at risk. Contact TourDay Team as soon as possible.\n\nThanks,\nTourDay Team"
                    async_send_mail(subject, message,
                                    EMAIL_HOST_USER, user.email)
                    user = authenticate(username=username, password=password1)
                    if user is not None:
                        login(request, user)
                        # Password changed
                        return JsonResponse({'status': 200})
                    else:
                        raise ValueError

                else:
                    raise ValueError
            except:
                return JsonResponse({'status': 404})  # bad request

        else:
            return JsonResponse({'status': 400})  # bad request
    return render(request, '_auth/reset_password.html', {'slug': slug})


def id_logout(request):
    logout(request)
    return redirect("login_page")


def checkusername(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()

        try:
            user = User.objects.get(username=username)
            return JsonResponse({'status': 200})  # username  exists
        except:
            return JsonResponse({'status': 404})  # username not exists


def checkemail(request):
    if request.method == "POST":
        email = request.POST.get('email').strip()

        try:
            user = User.objects.get(email=email)
            return JsonResponse({'status': 200})  # email  exists
        except:
            return JsonResponse({'status': 404})  # email not exists
