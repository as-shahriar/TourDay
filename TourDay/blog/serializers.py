from rest_framework import serializers
from .models import blogPost

class blogPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = blogPost
		fields =['id', 'slug', 'title', 'date', 'description', 'image', 'division']

class blogCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = blogPost
		fields = ['title', 'description', 'image', 'division']
		