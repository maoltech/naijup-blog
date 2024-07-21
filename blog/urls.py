from django.urls import path
from .views import BlogPostController, BlogPostByTitleView, MyBlogPostController, LatestBlogPostView, CommentDetailView, CommentListView, LikeDetailView, LikeListView, PostBookmarkView, LatestPostByCategoryView 

urlpatterns = [
    path('', BlogPostController.as_view(), name='blog_post_list'),
    path('<int:post_id>/', BlogPostController.as_view(), name='blog_post_detail'),
    path('my-posts/', MyBlogPostController.as_view(), name='my_blog_posts'),
    path('latest-posts/', LatestBlogPostView.as_view(), name='latest_blog_posts'),
    path('latest-posts/category/<str:category>/', LatestPostByCategoryView.as_view(), name='latest_blog_posts_category'),
    path('<int:post_id>/comments/', CommentListView.as_view(), name='comment_list'),
    path('<int:post_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment_detail'),
    path('<int:post_id>/likes/', LikeListView.as_view(), name='like_list'),
    path('<int:post_id>/likes/<int:like_id>/', LikeDetailView.as_view(), name='like_detail'),
    path('bookmarks/', PostBookmarkView.as_view(), name='post_bookmark_list'),
    path('bookmarks/<int:bookmark_id>/', PostBookmarkView.as_view(), name='post_bookmark_detail'),
    path('post/title/<str:title>/', BlogPostByTitleView.as_view(), name='blog_post_by_title')
]
