from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tweet,Comment,Retweet
from accounts.serializer import ProfileModelSerializer

User = get_user_model()

class TweetSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    update_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ['id','user_tweet']
        fields = ('id','text','user_tweet','created_on','tweet_img','update_on','tweet_like')
        

class CommentSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    
    class Meta:
        model = Comment
        read_only_fields = ['id','user_comment','tweet']
        fields = ('id','text','user_comment','created_on','comment_img','tweet','comment_like')
        

class RetweetSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    
    class Meta:
        model = Retweet
        read_only_fields = ['id','retweet_user','user_tweet']
        fields = ('id','text','retweet_user','created_on','user_tweet','retweet_like')
        

class TweetModelSerializer(serializers.ModelSerializer):
    tweet_user = ProfileModelSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields=('id','text','user_tweet',"tweet_user",'created_on','tweet_img','update_on','tweet_like')
        read_only_fields = ['id','user_tweet']


class CommentModelSerializer(serializers.ModelSerializer):
    comment_user = ProfileModelSerializer(read_only=True)
    class Meta:
        model = Comment
        fields=('id','text','user_comment','comment_user','created_on','comment_img','tweet','comment_like')
        read_only_fields = ['id','user_comment']

class RetweetModelSerializer(serializers.ModelSerializer):
    user_retweet = ProfileModelSerializer(read_only=True)
    class Meta:
        model = Retweet
        fields=('id','text','retweet_user','user_retweet','created_on','user_tweet','retweet_like')
        read_only_fields = ['id','retweet_user']

class TweetCommentSerializer(serializers.ModelSerializer):
    tweet_user = ProfileModelSerializer(read_only=True)
    comments=CommentModelSerializer(read_only=True,many=True)
    
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    update_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ['id','user_tweet']
        fields = ('id','text','user_tweet','tweet_user','created_on','tweet_img','update_on','tweet_like','comments')
        
class RetweetTweetSerializer(serializers.ModelSerializer):
    user = ProfileModelSerializer(read_only=True)
    retweets= RetweetModelSerializer(read_only=True,many=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    update_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ['id','user_tweet']
        fields = ('id','text','user_tweet','user','created_on','tweet_img','update_on','tweet_like','retweets')