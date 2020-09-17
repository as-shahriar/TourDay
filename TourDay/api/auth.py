
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .auth_serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from user_profile.models import Profile


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        profile = Profile(email=user.email, user=user)
        profile.save()
        return Response({
            'token': token.key,
        }, status=status.HTTP_201_CREATED)
