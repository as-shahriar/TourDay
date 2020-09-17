
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .auth_serializer import ProfileSerializer, ProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from user_profile.models import Profile
from rest_framework.parsers import FormParser, MultiPartParser


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        is_completed = False
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            profile = Profile(user=request.user, email=request.user.email)
            profile.save()
        if profile.name != None and profile.email != None and profile.fb != None and profile.bio != None and profile.city != None:
            is_completed = True
        data = ProfileSerializer(profile).data
        return Response({
            'profile': data,
            'is_completed': is_completed
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        name = serializer.data.get('name')
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        bio = serializer.data.get('bio')
        city = serializer.data.get('city')
        fb = serializer.data.get('fb')
        insta = serializer.data.get('insta')
        profile = Profile.objects.get(user=request.user)

        if name != None:
            profile.name = name
        if email != None:
            profile.email = email
            request.user.email = email
        if bio != None:
            profile.bio = bio
        if city != None:
            profile.city = city
        if fb != None:
            profile.fb = fb
        if insta != None:
            profile.insta = insta

        if password != None:
            request.user.set_password(password)

        profile.save()
        request.user.save()

        return Response({

        }, status=status.HTTP_200_OK)
