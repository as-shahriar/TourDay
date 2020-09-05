import json
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from .models import Profile, Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login
from utils import async_send_mail, districts, number_to_location
from TourDay.settings import EMAIL_HOST_USER
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


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


@login_required
def portfolio(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        try:
            nav_img = Profile.objects.get(user=request.user).picture.url
        except:
            nav_img = None
        return render(request, 'profile/portfolio.html', {
            'profile': profile,
            'districts': districts,
            "nav_img": nav_img,
            'is_profile': True,
            'user_obj': user
        })
    except:
        try:
            nav_img = Profile.objects.get(user=request.user).picture.url
        except:
            nav_img = None

        return render(request, 'profile/portfolio.html', {
            "nav_img": nav_img,
            'is_profile': False
        })


class PostList(APIView, LimitOffsetPagination):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    #pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        instance = Post.objects.filter(user=user).order_by("-date")
        instance = self.paginate_queryset(instance, request, view=self)
        for i in instance:
            i.location = number_to_location(i.location)

        serializer = self.serializer_class(instance, many=True)

        return self.get_paginated_response(serializer.data)


@csrf_exempt
@login_required
def like_event(request):
    if request.method == "POST":
        post_id = request.POST.get("id")
        try:
            post = Post.objects.get(id=post_id)
            if post.likes.all().filter(id=request.user.id).exists():  # user already liked
                post.likes.remove(request.user)

            else:
                post.likes.add(request.user)

            post.save()
            return JsonResponse({"id": post.id, "status": 200})
        except:
            return JsonResponse({"status": 404})
    return JsonResponse({"Error": "Only Post Request is Accepteble"})


@csrf_exempt
@login_required
def add_post(request):
    if request.method == "POST":
        post_text = request.POST.get("post")
        date = request.POST.get("date")
        location = request.POST.get("location")
        image = request.FILES.get("image")
        if post_text == "" or date == "" or location == "":
            return JsonResponse({"status": 400})

        post = Post()
        post.user = request.user
        post.post = post_text.strip()
        post.date = date
        post.location = location
        post.image = image
        post.save()
        return JsonResponse({
            "id": post.id,
            "image": post.image.url,
            "location": number_to_location(post.location),
            "status": 201
        })

    return JsonResponse({"Error": "Only Post Request is Accepteble"})


@csrf_exempt
@login_required
def delete_post(request):
    if request.method == "POST":
        post_id = request.POST.get("id")
        post = Post.objects.get(id=post_id)
        if request.user != post.user:
            return JsonResponse({"status": 403})
        post.delete()
        return JsonResponse({"status": 200})

    return JsonResponse({"Error": "Only Post Request is Accepteble"})


def get_map_data(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(user=user)
    visited = []
    for i in posts:
        if i.location not in visited:
            visited.append(i.location)

    return JsonResponse({"visited": visited, "status": 200})
