from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime

# Create your models here.
User = get_user_model()

def return_tweet_image_path(instance,filename):
    ext = filename.split('.')[-1]
    return '/'.join(['tweet',str(instance.id).zfill(5)+str(instance.user_tweet.id).zfill(10)+str(instance.created_on)+str(".")+str(ext)])

def return_comment_image_path(instance,filename):
    ext = filename.split('.')[-1]
    return '/'.join(['comment',str(instance.tweet.id).zfill(10)+str(instance.user_comment.id).zfill(10)+str(instance.created_on)+str(".")+str(ext)])

class Tweet(models.Model):
    text = models.TextField(
        verbose_name="tweet",max_length=500
    )
    tweet_user = models.ForeignKey(
        User,
        related_name='tweet_user',
        on_delete=models.CASCADE
    )
    tweet_img = models.ImageField(
        verbose_name="tweet image",
        blank=True,
        null=True,
        upload_to=return_tweet_image_path
    )
    created_on = models.DateTimeField(
        verbose_name="tweet date",
        auto_now_add=True
    )
    update_on = models.DateTimeField(
        verbose_name="tweet edit",
        default=timezone.now,
        null=True
    )
    tweet_like = models.ManyToManyField(
        User,
        related_name="tweet_like",
        blank=True    
    )
    
    def __str__(self):
        return  str(self.id)+" : "+self.text
    
class Comment(models.Model):
    text = models.TextField(
        verbose_name="comment",max_length=500
    )
    comment_user = models.ForeignKey(
        User,
        related_name="comment_user",
        on_delete=models.CASCADE,
    )
    tweet = models.ForeignKey(
        Tweet,
        related_name="user_tweet_comment",
        on_delete=models.CASCADE
    )
    comment_img = models.ImageField(
        verbose_name="comment image",
        blank=True,
        null=True,
        upload_to=return_comment_image_path
    )
    created_on=models.DateTimeField(
        auto_now_add=True
    )
    comment_like = models.ManyToManyField(
        User,
        related_name="comment_like",
        blank=True    
    )
    update_on = models.DateTimeField(
        verbose_name="comment edit",
        default=timezone.now,
        null=True
    )
    
    def __str__(self):
        return str(self.id)+" : "+self.text

class Retweet(models.Model):
    
    retweet_user = models.ForeignKey(
        User,
        related_name="retweet_user",
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name="retweet",
        max_length=500
    )
    tweet = models.ForeignKey(
        Tweet,
        related_name="user_tweet_retweet",
        on_delete=models.CASCADE
    )
    retweet_like= models.ManyToManyField(
        User,
        related_name="retweet_like",
        blank=True    
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.id)+" : "+self.text