from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from apicfg import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .views import TweetModelView,CommentModelView,RetweetModelView,TweetListView,MyTweetProfileView,TweetProfileModelView,TweetRetrieveView,CommentListView,CommentRetrieveView,TweetCommentModelView,TweetRetweetModelView

app_name='tweets'
router = DefaultRouter()
router.register('v1/tweet',TweetModelView)
router.register('v1/comment',CommentModelView)
router.register('v1/retweet',RetweetModelView)
router.register('v3/tweets/profiles',TweetProfileModelView)
router.register('v3/tweets/comment',TweetCommentModelView)
router.register('v3/tweets/retweets',TweetRetweetModelView)

urlpatterns = [
    path('v2/tweets/list/',TweetListView.as_view(),name="tweetlist"),
    path('v2/tweets/retrieve/',TweetRetrieveView.as_view(),name="tweetritrieve"),
    path('v2/comments/list/',CommentListView.as_view(),name="commentlist"),
    path('v2/comments/retrieve/',CommentRetrieveView.as_view(),name="commentretrieve"),
    path('v4/mytweets/list/',MyTweetProfileView.as_view(),name="mytweets"),
    path('',include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)