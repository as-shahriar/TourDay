from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login
from utils import async_send_mail,districts
from TourDay.settings import EMAIL_HOST_USER
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.models import User


@login_required
def edit_profile(request):

    is_complete = False
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.name != None and profile.email != None and profile.fb != None and profile.bio != None and profile.city != None:
            is_complete = True
    except:
        profile = Profile(user=request.user, email=request.user.email)
        profile.save()
    context = {
        "profile": profile,
        "is_complete": is_complete,
        "nav_img": profile.picture.url,
    }
    return render(request, "profile/profile.html", context)


@login_required
def add_info(request, param):
    if request.method == "POST":
        if 'data' in request.POST:
            data = request.POST.get('data').strip()
        profile = Profile.objects.get(user=request.user)
        if param == "name" and data != "":
            if profile.name != data:
                profile.name = data
                profile.save()
            return JsonResponse({
                "status": 201,
            })
        elif param == "email" and data != "":
            try:
                if profile.email != data:
                    old_email = profile.email
                    profile.email = data
                    profile.save()
                    subject = "Success! Email Changed | TourDay"
                    message = f"Hi {request.user.username},\nSuccess! Your Email has been changed!\n\nYour new email address is {profile.email}.\n\nIf you didn't changed your email, then your account is at risk. Contact TourDay Team as soon as possible.\n\nThanks,\nTourDay Team"
                    async_send_mail(subject, message,
                                    EMAIL_HOST_USER, old_email)

                    subject = "Success! Email Added | TourDay"
                    message = f"Hi {request.user.username},\nSuccess! This email has been added as your default email for TourDay.\n\nIf you received this email but didn't register for an TourDay account, something's gone wrong, Reply to this email to de-activate and close this account.\n\nThanks,\nTourDay Team"
                    async_send_mail(subject, message,
                                    EMAIL_HOST_USER, profile.email)
                return JsonResponse({
                    "status": 201,
                })
            except:
                return JsonResponse({
                    "status": 400,
                })

        elif param == "fb" and data != "":
            if profile.fb != data:
                profile.fb = data
                profile.save()
            return JsonResponse({
                "status": 201,
            })

        elif param == "password" and data != "":
            user = request.user
            user.set_password(data)
            user.save()
            login(request, user)
            subject = "Success! Password Changed | TourDay"
            message = f"Hi {user.username},\nSuccess! Your Password has been changed!\n\nIf you didn't changed your password, then your account is at risk. Contact TourDay Team as soon as possible.\n\nThanks,\nTourDay Team"
            async_send_mail(subject, message,
                            EMAIL_HOST_USER, request.user.email)
            return JsonResponse({
                "status": 201,
            })

        elif param == "bio" and data != "":
            if profile.bio != data:
                profile.bio = data
                profile.save()
            return JsonResponse({
                "status": 201,
            })

        elif param == "city" and data != "":
            if profile.city != data:
                profile.city = data
                profile.save()
            return JsonResponse({
                "status": 201,
            })

        elif param == "picture":
            image_data = request.POST.get("picture")
            format, imgstr = image_data.split(';base64,')
            print("format", format)
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = "'myphoto." + ext
            profile.picture.save(file_name, data, save=True)

            return JsonResponse({
                "status": 201,
                "new_img": profile.picture.url,

            })
        else:
            return JsonResponse({}, status=404)


def portfolio(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        return render(request, 'profile/portfolio.html', {
            'profile': profile,
            'districts': districts
        })
    except:
        return render(request, 'profile/portfolio.html')
