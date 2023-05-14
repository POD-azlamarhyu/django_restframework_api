from django.shortcuts import render
from rest_framework import permissions,status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.cache import cache_page
from django.db.models import Q,Prefetch,F
from django.db import connection
from django.forms.models import model_to_dict
import json
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse,Http404
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,BasePermission
from .models import Tweet,Comment,Retweet
from .serializer import TweetSerializer,CommentSerializer,RetweetSerializer,TweetModelSerializer,CommentModelSerializer,RetweetModelSerializer,TweetCommentSerializer,RetweetTweetSerializer

User = get_user_model()

class TweetModelView(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    
    def perform_create(self,serializer):
        serializer.save(user_tweet=self.request.user)

class CommentModelView(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self,serializer):
        serializer.save(user_comment=self.request.user)
        
class RetweetModelView(viewsets.ModelViewSet):
    queryset=Retweet.objects.all()
    serializer_class = RetweetSerializer
    
    def perform_create(self,serializer):
        serializer.save(retweet_user=self.request.user)

class TweetListView(ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def list(self,request):
        queryset=self.get_queryset()
        serializer=TweetSerializer(queryset,many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class TweetRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def get(self,request,pk):
        queryset=self.get_queryset(pk=pk)
        serializer=TweetSerializer(queryset,many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        
class CommentListView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self,request):
        queryset=self.get_queryset()
        serializer=CommentSerializer(queryset,many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
class CommentRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self,request,pk):
        queryset=self.get_queryset(pk=pk)
        serializer=CommentSerializer(queryset,many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
class TweetProfileModelView(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('tweet').all()
    serializer_class=TweetModelSerializer
    
class TweetCommentModelView(viewsets.ModelViewSet):
    queryset = Tweet.objects.select_related('user').prefetch_related('comment').all()
    serializer_class=TweetCommentSerializer
    
class TweetRetweetModelView(viewsets.ModelViewSet):
    queryset=Tweet.objects.select_related('user').prefetch_related('retweet').all()
    serializer_class=RetweetTweetSerializer

class MyTweetProfileView(APIView):
    
    def get(self,request):
        try:
            uid = request.user.id
            query = '''
                select
                    ui.id,
                    ui.email,
                    ui.is_staff,
                    ui.is_superuser,
                    upi.nickname,
                    upi.account_id,
                    upi.icon,
                    upi.created_on,
                    upi.bio,
                    upi.link,
                    ti.id,
                    ti.text,
                    ti.tweet_img,
                    ti.created_on,
                    ti.update_on,
                    (select
                        count(ttl.user_id)
                    from
                        tweets_tweet_tweet_like as ttl
                    where
                        ttl.tweet_id = ti.id
                    ) as likes
                    
                from
                    tweets_tweet as ti
                left join
                    accounts_user as ui
                on
                    ti.user_tweet_id = ui.id
                left join 
                    accounts_userprofile as upi
                on
                    ui.id = upi.user_profile_id
                where
                    ui.id = %s
                order by
                    ti.created_on asc
            '''
            cursor = connection.cursor()
            cursor.execute(query,(uid,))
            columns = [col[0] for col in cursor.description]
            print(cursor.description)
            tweet_dict = [
                dict(zip(columns,row))
                for row in cursor.fetchall()
            ]
            return Response(
                data={
                    "result":"success",
                    "content":tweet_dict
                },
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(
                data={
                    "result":"success",
                    "content":"None"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                data={
                    "result":"error",
                    "content":"問題が発生"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )