
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import ProfileSerializer, ProfileUpdateSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_profile.models import Profile, Post
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
            'username': request.user.username,
            'id': request.user.id,
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
        picture = serializer.data.get('picture')
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

        if picture != None:
            print(picture)
            profile.picture = picture

        if password != None:
            request.user.set_password(password)

        profile.save()
        request.user.save()

        return Response({

        }, status=status.HTTP_200_OK)


class PostWrite(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({
            'post_id': serializer.data.get('id'),
            'image': serializer.data.get('image')
        }, status=status.HTTP_200_OK)


class PostDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = request.data.get('id')

        try:
            post = Post.objects.get(id=id)
            if post.user == request.user:
                post.delete()
            return Response({}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsByID(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            profile = Profile.objects.get(user__id=id)
            data = ProfileSerializer(profile).data
            return Response({'profile': data}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            profile = Profile.objects.get(user__username=username)
            data = ProfileSerializer(profile).data
            return Response({'profile': data}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
            if post.likes.all().filter(id=request.user.id).exists():  # user already liked
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            post.save()
            return Response({'like_count': post.likes.count()}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
