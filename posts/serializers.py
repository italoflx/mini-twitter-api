from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author','title', 'content', 'image', 'hashtags','created_at', 'updated_at', 'likes']
        read_only_fields = ['likes']  

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        if len(value) > 500:
            raise serializers.ValidationError("Content cannot be longer than 500 characters.")
        return value
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("The title cannot be empty.")
        if len(value) > 500:
            raise serializers.ValidationError("Content cannot be longer than 500 characters.")
        return value

    def validate_image(self, value):
        if value:
            if not value.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise serializers.ValidationError("The file must be a valid image (PNG, JPG, JPEG, GIF).")
        return value
