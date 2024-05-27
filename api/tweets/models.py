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
        auto_now_add=True,
        editable=False
    )
    update_on = models.DateTimeField(
        verbose_name="tweet edit",
        default=timezone.now,
        null=True
    )
    tweet_like = models.ManyToManyField(
        User,
        through='TweetLikeTBL',
        related_name="tweet_like_tbl"
    )
    
    def __str__(self):
        return  str(self.id)+" : "+self.text

class TweetLikeTBL(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name="tweet_like_id",
        verbose_name="tweet id"
    )
    tweet_like_user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tweet_like_user_id",
        verbose_name="user id"
    )
    created_on = models.DateTimeField(
        verbose_name="like date",
        auto_now_add=True,
        editable=False
    )
    class Meta:
        unique_together=('tweet','tweet_like_user')
    
    def __str__(self) -> str:
        return f'{self.tweet}:{self.tweet_like_user}'

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
        auto_now_add=True,
        verbose_name="comment date",
        editable=False
    )
    comment_like = models.ManyToManyField(
        User,
        related_name="comment_like_tbl",
        through='CommentLikeTBL',
    )
    update_on = models.DateTimeField(
        verbose_name="comment edit",
        default=timezone.now,
        null=True
    )
    
    def __str__(self):
        return str(self.id)+" : "+self.text

class CommentLikeTBL(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="comment_like_id",
        verbose_name="comment id"
    )
    comment_like_user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_like_user_id",
        verbose_name="user id"
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name="comment date",
        editable=False
    )
    class Meta:
        unique_together=('comment','comment_like_user')
    
    def __str__(self) -> str:
        return f'{self.comment}:{self.comment_like_user}'

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
        through='RetweetLikeTBL',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="retweet date"
    )
    update_on = models.DateTimeField(
        verbose_name="retweet edit",
        default=timezone.now,
        null=True
    )
    def __str__(self):
        return str(self.id)+" : "+self.text

class RetweetLikeTBL(models.Model):
    retweet = models.ForeignKey(
        Retweet,
        on_delete=models.CASCADE,
        related_name="retweet_like_id",
        verbose_name="retweet id"
    )
    retweet_like_user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="retweet_like_user_id",
        verbose_name="user id"
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name="retweet date",
        editable=False
    )
    class Meta:
        unique_together=('retweet','retweet_like_user')
    
    def __str__(self) -> str:
        return f'{self.retweet}:{self.retweet_like_user}'