from rest_framework import serializers
from .models import BlogPost
from .models import Comment
from .models import Like
from .models import PostBookmark

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'description', 'content', 'publication_date', 'file', 'category', 'tags', 'image_links', 'author', 'publication_date', 'update_date']
        read_only_fields = ['publication_date', 'update_date', 'author']

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