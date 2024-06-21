from django.contrib import admin
from .models import BlogPost, Comment, Like, PostBookmark

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'update_date')
    search_fields = ('title', 'author__username', 'category')
    list_filter = ('category', 'author')
    ordering = ('-publication_date',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'publish_date')
    search_fields = ('post__title', 'author__username', 'content')
    list_filter = ('publish_date', 'author')
    ordering = ('-publish_date',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)

class PostBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(PostBookmark, PostBookmarkAdmin)
