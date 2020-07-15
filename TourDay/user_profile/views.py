from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required


@login_required
def edit_profile(request):
    profile = None
    is_complete = False
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.name != None and profile.email != None and profile.fb != None and profile.bio != None and profile.city != None:
            is_complete = True
    except:
        pass
    context = {
        "profile": profile,
        "is_complete": is_complete
    }
    return render(request, "profile/profile.html", context)
