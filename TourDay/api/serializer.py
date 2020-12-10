from event.models import Event, Transactions
from rest_framework import serializers
from django.contrib.auth.models import User
from user_profile.models import Profile, Post
from django.core.validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = self.initial_data.get('email')
        password = self.initial_data.get('password')
        the_user = User.objects.filter(email=email)

       # if len(password) <= 7:
        #    raise serializers.ValidationError('Password length must be 8 Character!')
        if the_user.count() == 0:
            return data
        else:
            raise serializers.ValidationError('Email Already Used!')

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user','username', 'name', 'email', 'fb',
                  'insta', 'city', 'bio', 'picture']
    
    def get_username(self,instance):
        return instance.user.username        


class ProfileUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    fb = serializers.CharField()
    insta = serializers.CharField()
    password = serializers.CharField()
    bio = serializers.CharField()
    city = serializers.CharField()
    picture = serializers.ImageField()

    def validate(self, data):
        email = self.initial_data.get('email')
        try:
            validate_email(email)
        except:
            raise serializers.ValidationError('Invalid Email Address')
        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['user']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('__all__')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('__all__')
