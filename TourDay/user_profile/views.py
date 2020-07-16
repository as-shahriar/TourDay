from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login


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
        "is_complete": is_complete
    }
    return render(request, "profile/profile.html", context)


@login_required
def add_info(request, param):
    if request.method == "POST":

        data = request.POST.get('data').strip()
        profile = Profile.objects.get(user=request.user)
        if param == "name" and data != "":
            profile.name = data
            profile.save()
            return JsonResponse({
                "status": 201,
            })
        elif param == "email" and data != "":
            try:
                profile.email = data
                profile.save()
                return JsonResponse({
                    "status": 201,
                })
            except:
                return JsonResponse({
                    "status": 400,
                })

        elif param == "fb" and data != "":
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
            return JsonResponse({
                "status": 201,
            })

        elif param == "bio" and data != "":
            profile.bio = data
            profile.save()
            return JsonResponse({
                "status": 201,
            })

        elif param == "city" and data != "":
            profile.city = data
            profile.save()
            return JsonResponse({
                "status": 201,
            })
        else:
            return JsonResponse({}, status=404)
