from django.shortcuts import render
from rest_framework import permissions,status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.cache import cache_page
from django.db.models import Q,Prefetch,F,Count,FilteredRelation,Max,Min,Avg,Sum,Subquery,OuterRef,Case,When,Value
from django.db import connection
from django.forms.models import model_to_dict
from django.db.models.expressions import RawSQL
import json
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse,Http404
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,BasePermission
from .models import Tweet,Comment,Retweet,TweetLikeTBL,RetweetLikeTBL,CommentLikeTBL
from .serializer import TweetSerializer,CommentSerializer,RetweetSerializer,TweetModelSerializer,CommentModelSerializer,RetweetModelSerializer,TweetCommentSerializer,RetweetTweetSerializer
from django.db.models.functions import TruncDate
from django.utils.decorators import method_decorator
User = get_user_model()

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns,row))
        for row in cursor.fetchall()
    ]

class TweetModelView(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated,]
    def perform_create(self,serializer):
        serializer.save(user_tweet=self.request.user)

class CommentModelView(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]
    def perform_create(self,serializer):
        serializer.save(user_comment=self.request.user)
        
class RetweetModelView(viewsets.ModelViewSet):
    queryset=Retweet.objects.all()
    serializer_class = RetweetSerializer
    permission_classes = [IsAuthenticated,]
    def perform_create(self,serializer):
        serializer.save(retweet_user=self.request.user)

class TweetListView(ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated,]
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
    permission_classes = [IsAuthenticated,]
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
    permission_classes = [IsAuthenticated,]
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
    queryset = Tweet.objects.all().select_related('user_tweet').annotate()
    serializer_class=TweetModelSerializer
    permission_classes = [IsAuthenticated,]
class TweetCommentModelView(viewsets.ModelViewSet):
    queryset = Tweet.objects.select_related('user').prefetch_related('comment').all()
    serializer_class=TweetCommentSerializer
    permission_classes = [IsAuthenticated,]
class TweetRetweetModelView(viewsets.ModelViewSet):
    queryset=Tweet.objects.select_related('user').prefetch_related('retweet').all()
    serializer_class=RetweetTweetSerializer
    permission_classes = [IsAuthenticated,]
    


class MyTweetProfileView(APIView):
    permission_classes = [IsAuthenticated,]
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
            cursor.execute(query % (uid))
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
class TweetJoinModelView(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated,]

    @action(methods=['GET'],detail=True)
    def tweet_list(self,request,pk=None):
        query = Tweet.objects.all().annotate(
            user=FilteredRelation(
                'tweet_user'
            )
        )
        if query is not None:
            return Response(
                data={
                    'result':'success',
                    'content':list(query.values())
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'result':'success',
                    'content':'検索した対象は見つかりませんでした．'
                },
                status=status.HTTP_200_OK
            )

class TweetTextSearchView(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated,]
    
    @action(methods=['GET'],detail=True)
    def text_single(self,request,pk=None):
        keywords = str(request.data['keywords']).split(" ")
        query = Tweet.objects.select_related().filter(text__contains=keywords)

        if query is not None:
            return Response(
                data={
                    'result':'success',
                    'content':list(query.values())
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'result':'success',
                    'content':'検索した対象は見つかりませんでした．'
                },
                status=status.HTTP_200_OK
            )
            
    @action(methods=['GET'],detail=True)
    def multi_param(self,request,pk=None):
        keyword = str(request.data['keywords']).split(" ")
        date = request.data['date']
        query = Tweet.objects.select_related().filter(
                Q(text__contains=keyword)|
                Q(created_on__glt=date)
            )
        if query is not None:
            return Response(
                data={
                    'result':'success',
                    'content':list(query.values())
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'result':'success',
                    'content':'検索した対象は見つかりませんでした．'
                },
                status=status.HTTP_200_OK
            )
    @action(methods=['GET'],detail=False)
    def multi_like_param(self,request):
        likes = request.data['like']
        query = Tweet.objects.select_related("tweet_user").annotate(
            like_count = Count('tweet_like')
        ).filter(like_count__gte=likes)
        print(query)
        if query is not None:
            return Response(
                data={
                    'result':'success',
                    'content':list(query.values())
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'result':'success',
                    'content':'検索した対象は見つかりませんでした．'
                },
                status=status.HTTP_200_OK
            )


class TweetAndUserProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get_likes_list(self):
        query = '''
            select
                *
            from
                tweets_tweet_tweet_like as ttl
        '''
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        dicts = [
            dict(zip(columns,row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        return dicts
    def get(self,request):
        try:
            query = '''
                select
                    ui.id as user_id,
                    ui.email,
                    ui.is_staff,
                    ui.is_superuser,
                    upi.nickname,
                    upi.account_id,
                    upi.icon,
                    upi.created_on,
                    upi.bio,
                    upi.link,
                    ti.id as tweet_id,
                    ti.text,
                    ti.tweet_img,
                    ti.created_on,
                    ti.update_on
                from
                    tweets_tweet as ti
                left join
                    accounts_user as ui
                on
                    ti.tweet_user_id = ui.id
                left join 
                    accounts_userprofile as upi
                on
                    ui.id = upi.user_profile_id
                order by
                    ti.created_on asc
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            
            tweet_dict = [
                dict(zip(columns,row))
                for row in cursor.fetchall()
            ]
            cursor.close()
            like_list = self.get_likes_list()
            for i in range(len(tweet_dict)):
                likes_user_list = []
                for like in like_list[:]:
                    if tweet_dict[i]["tweet_id"] == like["tweet_id"]:
                        likes_user_list.append(like["user_id"])
                        # del like_list[j]
                        like_list.remove(like)
                        
                tweet_dict[i]["like"] = likes_user_list
            
            
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
class CommentAndUserProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    def get_likes_list(self):
        query = '''
            select
                *
            from
                tweets_comment_comment_like as tcl
        '''
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        dicts = [
            dict(zip(columns,row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        return dicts
    def get(self,request):
        try:
            query = '''
                select
                    ui.id as user_id,
                    ui.email,
                    ui.is_staff,
                    ui.is_superuser,
                    upi.nickname,
                    upi.account_id,
                    upi.icon,
                    upi.created_on,
                    upi.bio,
                    upi.link,
                    ci.id as comment_id,
                    ci.text,
                    ci.comment_img,
                    ci.created_on,
                    ci.update_on
                from
                    tweets_comment as ci
                left join
                    accounts_user as ui
                on
                    ci.comment_user_id = ui.id
                left join
                    accounts_userprofile as upi
                on
                    ui.id = upi.user_profile_id
                order by
                    ci.created_on asc
            '''
            
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            
            comment_dict = [
                dict(zip(columns,row))
                for row in cursor.fetchall()
            ]
            cursor.close()
            like_list = self.get_likes_list()
        
            for i in range(len(comment_dict)):
                likes_user_list = []
                for like in like_list[:]:
                    if comment_dict[i]["comment_id"] == like["comment_id"]:
                        likes_user_list.append(like["user_id"])
                        like_list.remove(like)
                        
                comment_dict[i]["like"] = likes_user_list
            
            
            return Response(
                data={
                    "result":"success",
                    "content":comment_dict
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
            
class RetweetAndProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    def get_likes_list(self):
        query = '''
            select
                *
            from
                tweets_retweet_retweet_like as trl
        '''
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        dicts = [
            dict(zip(columns,row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        return dicts
    def get(self,request):
        try:
            query = '''
                select
                    ui.id as user_id,
                    ui.email,
                    ui.is_staff,
                    ui.is_superuser,
                    upi.nickname,
                    upi.account_id,
                    upi.icon,
                    upi.created_on as up_created_on,
                    upi.bio,
                    upi.link,
                    ri.id as retweet_id,
                    ri.text as retweet_text,
                    ri.created_on as rt_created_on,
                    ti.id as tweet_id,
                    ti.text as tweet_text,
                    ti.tweet_img,
                    ti.created_on as tweet_created_on,
                    ti.update_on
                from
                    tweets_retweet as ri
                left join
                    accounts_user as ui
                on
                    ri.retweet_user_id = ui.id
                left join
                    accounts_userprofile as upi
                on
                    ui.id = upi.user_profile_id
                left join
                    tweets_tweet as ti
                on
                    ri.tweet_id = ti.id
                order by
                    rt_created_on asc
                limit 10
            '''
            
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            
            retweet_dict = [
                dict(zip(columns,row))
                for row in cursor.fetchall()
            ]
            cursor.close()
            like_list = self.get_likes_list()
        
            for i in range(len(retweet_dict)):
                likes_user_list = []
                for like in like_list[:]:
                    if retweet_dict[i]["retweet_id"] == like["retweet_id"]:
                        likes_user_list.append(like["user_id"])
                        like_list.remove(like)
                        
                retweet_dict[i]["like"] = likes_user_list
            
            
            return Response(
                data={
                    "result":"success",
                    "content":retweet_dict
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

class TweetCommentView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        if request.data["tid"]:
            tweet_id = request.data["tid"]
        elif request.query_params.get("tid",None):
            tweet_id = request.query_params.get("tid",None)
            
        query = '''
            select
                ui.id as user_id,
                ui.email,
                ui.is_staff,
                ui.is_superuser,
                upi.nickname,
                upi.account_id,
                upi.icon,
                upi.created_on,
                upi.bio,
                upi.link,
                ti.id as tweet_id,
                ti.text,
                ti.tweet_img,
                ti.created_on,
                ti.update_on
            from
                tweets_tweet as ti
            left join
                accounts_user as ui
            on
                ti.tweet_user_id = ui.id
            left join 
                accounts_userprofile as upi
            on
                ui.id = upi.user_profile_id
            where
                ti.id = %s
        '''
        cursor = connection.cursor()
        cursor.execute(query % (tweet_id))
        columns = [col[0] for col in cursor.description]
        res = cursor.fetchone()

        tweet_dict = dict(zip(columns,res))
        
        query = '''
                select
                    ui.id as user_id,
                    ui.email,
                    ui.is_staff,
                    ui.is_superuser,
                    upi.nickname,
                    upi.account_id,
                    upi.icon,
                    upi.created_on,
                    upi.bio,
                    upi.link,
                    ci.id as comment_id,
                    ci.text,
                    ci.comment_img,
                    ci.created_on,
                    ci.update_on
                from
                    tweets_comment as ci
                left join
                    accounts_user as ui
                on
                    ci.comment_user_id = ui.id
                left join
                    accounts_userprofile as upi
                on
                    ui.id = upi.user_profile_id
                where
                    ci.tweet_id = %s
                limit 10
            '''
        cursor.execute(query % (tweet_id))
        columns = [col[0] for col in cursor.description]
        comment_dict = [
            dict(zip(columns,row))
            for row in cursor.fetchall()
        ]
        cursor.close()
        tweet_dict["comments"] = comment_dict
        print(tweet_dict) 
        return Response(
                data={
                    "result":"success",
                    "content":tweet_dict
                },
                status=status.HTTP_200_OK
            )

class TweetLikeToggleView(APIView):
    permission_classes=[IsAuthenticated,]
    
    @method_decorator(csrf_protect)
    def post(self,request):
        try:
            user_id = request.user.id
            tweet_id = request.data["id"]
            tweet_like_recode=TweetLikeTBL.objects.filter(
                tweet_like_user=user_id,
                tweet=tweet_id
            ).first()
            
            if tweet_like_recode:
                tweet_like_recode.delete()
                content = "delete like info."
            else:
                new_tweet_like = TweetLikeTBL(
                    tweet_like_user=user_id,
                    tweet=tweet_id
                )
                
                new_tweet_like.save()
                content = "post like info."
            return Response(
                data={
                    "result":"success",
                    "content":content,
                    "data":{}
                },
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            print(ex)
            return Response(
                data={
                    "result":"error",
                    "content":"問題が発生"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentLikeToggleView(APIView):
    permission_classes=[IsAuthenticated,]
    
    @method_decorator(csrf_protect)
    def post(self,request):
        try:
            user_id = request.user.id
            comment_id = request.data["id"]
            comment_like_recode=CommentLikeTBL.objects.filter(
                comment_like_user=user_id,
                comment=comment_id
            ).first()
            
            if comment_like_recode:
                comment_like_recode.delete()
                content = "delete like info."
            else:
                new_comment_like = TweetLikeTBL(
                    comment_like_user=user_id,
                    comment=comment_id
                )
                
                new_comment_like.save()
                content = "post like info."
            return Response(
                data={
                    "result":"success",
                    "content":content,
                    "data":{}
                },
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            print(ex)
            return Response(
                data={
                    "result":"error",
                    "content":"問題が発生"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RetweetLikeToggleView(APIView):
    permission_classes=[IsAuthenticated,]
    
    @method_decorator(csrf_protect)
    def post(self,request):
        try:
            user_id = request.user.id
            retweet_id = request.data["id"]
            retweet_like_recode=RetweetLikeTBL.objects.filter(
                retweet_like_user=user_id,
                retweet=retweet_id
            ).first()
            
            if retweet_like_recode:
                retweet_like_recode.delete()
                content = "delete like info."
            else:
                new_retweet_like = TweetLikeTBL(
                    retweet_like_user=user_id,
                retweet=retweet_id
                )
                
                new_retweet_like.save()
                content = "post like info."
            return Response(
                data={
                    "result":"success",
                    "content":content,
                    "data":{}
                },
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            print(ex)
            return Response(
                data={
                    "result":"error",
                    "content":"問題が発生"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TweetWithUserModelView(APIView):
    permission_classes=[IsAdminUser,]
    
    def get(self,request):
        tweet_like_subquery=TweetLikeTBL.objects.values("id","tweet_id").annotate(tweet_like_count=Count("id")).order_by("tweet_id")
        tweet_like_cursor_subquery = '''
            select
                tweet_id,
                count(tweet_like_user_id) as tweet_like_count
            from
                tweet_like
            group by
                tweet_id
        '''
        cursor = connection.cursor()
        
        
        cursor_query='''
            select
                *
            from
                tweet
            left join
                accounts_user as au
            on
                tweet.tweet_user_id = au.id
            left join 
                user_profile as up
            on
                tweet.tweet_user_id = up.user_profile_id
            left join
                (
                    select
                        tweet_id,
                        count(tweet_like_user_id) as tweet_like_count
                    from
                        tweet_like
                    group by
                        tweet_id
                ) as tls
            on
                tweet.id = tls.tweet_id
        '''
        cursor.execute(cursor_query)
        tweet_like_list = dictfetchall(cursor)
        content="info."
        return Response(
                data={
                    "result":"success",
                    "content":content,
                    "data":tweet_like_list
                },
                status=status.HTTP_200_OK
            )
        