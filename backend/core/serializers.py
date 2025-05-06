from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BlogPost

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'email': obj.author.email,
            'full_name': obj.author.full_name
        }
