from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    fullname = models.CharField(
        max_length=200,
        blank=True,
        null=True
        )
    
    email = models.EmailField(
        max_length=200,
        null=True,
        blank=True
        )
    

    phone_no = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    profile_pic = models.ImageField(
        upload_to='profile_pic/',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.username


class FeedPost(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feed_posts'  
    )
    
    caption = models.TextField(blank=True, null=True)

    image = models.ImageField(
        upload_to='feedposts/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='liked_feedposts'  
    )

    def __str__(self):
        return f"{self.author.username}'s Post at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    



class FeedPostComment(models.Model):
    post = models.ForeignKey(
        'FeedPost',
        on_delete=models.CASCADE,
        related_name='feedpost_comments'  
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedpost_comments_made'
    )
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_feedpost_comments',
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author.username}'s Comment on FeedPost {self.post.id}"

    def is_reply(self):
        return self.parent is not None
