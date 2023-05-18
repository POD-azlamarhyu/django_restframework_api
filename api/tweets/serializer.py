from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tweet,Comment,Retweet
from accounts.serializer import ProfileModelSerializer,UserSerializer

User = get_user_model()

class TweetSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    update_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ['id','tweet_user']
        fields = ('id','text','tweet_user','created_on','tweet_img','update_on','tweet_like')
        

class CommentSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    
    class Meta:
        model = Comment
        read_only_fields = ['id','comment_user','tweet']
        fields = ('id','text','comment_user','created_on','comment_img','tweet','comment_like')
        

class RetweetSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    
    class Meta:
        model = Retweet
        read_only_fields = ['id','retweet_user','tweet_user']
        fields = ('id','text','retweet_user','created_on','tweet_user','retweet_like')
        

class TweetModelSerializer(serializers.ModelSerializer):
    tweet_user = ProfileModelSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields=('id','text','tweet_user',"tweet_user",'created_on','tweet_img','update_on','tweet_like')
        read_only_fields = ['id','tweet_user']

class TweetLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields=('id','tweet_like')
        read_only_fields = ['id']
class CommentModelSerializer(serializers.ModelSerializer):
    comment_user = ProfileModelSerializer(read_only=True)
    class Meta:
        model = Comment
        fields=('id','text','comment_user','comment_user','created_on','comment_img','tweet','comment_like')
        read_only_fields = ['id','comment_user']

class RetweetModelSerializer(serializers.ModelSerializer):
    user_retweet = ProfileModelSerializer(read_only=True)
    class Meta:
        model = Retweet
        fields=('id','text','retweet_user','user_retweet','created_on','tweet_user','retweet_like')
        read_only_fields = ['id','retweet_user']

class TweetCommentSerializer(serializers.ModelSerializer):
    tweet_user = ProfileModelSerializer(read_only=True)
    comments=CommentModelSerializer(read_only=True,many=True)
    
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    update_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ['id','tweet_user']
        fields = ('id','text','tweet_user','tweet_user','created_on','tweet_img','update_on','tweet_like','comments')
        
class RetweetTweetSerializer(serializers.ModelSerializer):
    user = ProfileModelSerializer(read_only=True)
    retweets= RetweetModelSerializer(read_only=True,many=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    update_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    class Meta:
        model = Tweet
        read_only_fields = ['id','tweet_user']
        fields = ('id','text','tweet_user','user','created_on','tweet_img','update_on','tweet_like','retweets')