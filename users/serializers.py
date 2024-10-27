from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'followers_count', 'followers', 'following']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})

        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def get_followers(self, obj):
        return [{"id": follower.id, "username": follower.username, "email": follower.email} for follower in obj.followers.all()]
    
    def get_following(self, obj):
        return [{"id": following.id, "username": following.username} for following in obj.following.all()]
