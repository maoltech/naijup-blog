import json
from rest_framework import serializers
from .models import BlogPost
from .models import Comment
from .models import Like
from .models import PostBookmark

class BlogPostSerializer(serializers.ModelSerializer):
    # tags = serializers.SerializerMethodField()  # Use a method to get tags
    # set_tags = serializers.ListField(write_only=True) 
    tags  = serializers.ListField(
        child=serializers.CharField(max_length=100)  # Define the field for each size in the list
    )
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'publication_date', 'file', 'category', 'tags', 'image_links', 'author', 'publication_date', 'update_date']
        extra_kwargs = {
            'file': {'required': False},
            'tags': {'required': False}
        }
        read_only_fields = ['publication_date', 'update_date', 'author']
    # def get_tags(self, obj):
    #     return json.loads(obj.tags)

    # # Override the `create` method to handle the `tags` field
    # def create(self, validated_data):
    #     tags = validated_data.pop('set_tags', [])
    #     blog_post = BlogPost.objects.create(**validated_data)
    #     blog_post.set_tags(tags)
    #     blog_post.save()
    #     return blog_post

    # # Override the `update` method to handle the `tags` field
    # def update(self, instance, validated_data):
    #     tags = validated_data.pop('set_tags', [])
    #     instance.set_tags(tags)
    #     return super().update(instance, validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['post', 'author', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['post', 'user', 'created_at']

class PostBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBookmark
        fields = ['id', 'user', 'post', 'created_at']