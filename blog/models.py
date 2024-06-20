from django.db import models
from user.models import User
from django.core.exceptions import ValidationError
import json
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.JSONField()
    description = models.TextField()
    category = models.CharField(max_length=159, default='General')
    tags = models.TextField(default=json.dumps([]), blank=True)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    file = models.CharField(max_length=255)
    image_links = models.JSONField(default=list)

    def set_tags(self, tags):
        if not isinstance(tags, list):
            raise ValidationError('Expected a list of strings')
        self.tags = json.dumps(tags)

    def get_tags(self):
        return json.loads(self.tags)

    def save(self, *args, **kwargs):
        if isinstance(self.tags, list):
            self.tags = json.dumps(self.tags)
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    post = models.ForeignKey(BlogPost, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"
    
class PostBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s bookmark for {self.post.title}"
