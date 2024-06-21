from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost, Comment, Like, PostBookmark
from .serializers import BlogPostSerializer, CommentSerializer, LikeSerializer, PostBookmarkSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
# import requests

class BlogPostController(APIView):

    def get(self, request):
        try:
            post = BlogPost.objects.get()
            serializer = BlogPostSerializer(post)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_author:
            raise PermissionError("You do not have permission to create blog posts.")
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        try:
            post = BlogPost.objects.get(pk=post_id, author=request.user)
            serializer = BlogPostSerializer(post)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class MyBlogPostController(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = BlogPost.objects.filter(author=request.user)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def put(self, request, post_id):
        try:
            post = BlogPost.objects.get(pk=post_id, author=request.user)
            serializer = BlogPostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id):
        try:
            post = BlogPost.objects.get(pk=post_id, author=request.user)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class LatestBlogPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LatestBlogPostView(APIView):
    pagination_class = LatestBlogPostPagination

    def get(self, request):
        paginator = self.pagination_class()
        latest_posts = BlogPost.objects.order_by('-publication_date')
        result_page = paginator.paginate_queryset(latest_posts, request)
        serializer = BlogPostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id, post_id=post_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id, post_id=post_id, author=request.user)
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id, post_id=post_id, author=request.user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class LikeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        likes = Like.objects.filter(post_id=post_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        like_data = {'post': post_id, 'user': request.user.id}
        serializer = LikeSerializer(data=like_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id, like_id):
        try:
            like = Like.objects.get(pk=like_id, post_id=post_id, user=request.user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PostBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostBookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        bookmarks = PostBookmark.objects.filter(user=request.user)
        serializer = PostBookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)

    def delete(self, request, bookmark_id):
        try:
            bookmark = PostBookmark.objects.get(pk=bookmark_id, user=request.user)
            bookmark.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PostBookmark.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class LatestPostByCategoryView(APIView):
    def get(self, request, category):
        try:
            latest_posts = BlogPost.objects.filter(category=category).order_by('-publication_date')[:5]  # Get latest 5 posts by category
            serializer = BlogPostSerializer(latest_posts, many=True)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
# class LiveMarkets(models.Model):
#     def get(self, request):