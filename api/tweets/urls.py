from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from apicfg import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .views import TweetModelView,CommentModelView,RetweetModelView,TweetListView,MyTweetProfileView,TweetProfileModelView,TweetRetrieveView,CommentListView,CommentRetrieveView,TweetCommentModelView,TweetRetweetModelView,TweetAndUserProfileView,TweetTextSearchView,TweetJoinModelView,CommentAndUserProfileView,RetweetAndProfileView,TweetCommentView,TweetLikeToggleView,CommentLikeToggleView,RetweetLikeToggleView,TweetWithUserModelView

app_name='tweets'
router = DefaultRouter()
router.register('v1/tweet',TweetModelView)
router.register('v1/comment',CommentModelView)
router.register('v1/retweet',RetweetModelView)
router.register('v3/tweets/profiles',TweetProfileModelView,basename="tweetprofile")
router.register('v3/tweets/comment',TweetCommentModelView,basename="tweetcomment")
router.register('v3/tweets/retweets',TweetRetweetModelView,basename="tweetretweet")
router.register('v5/list/tweet/research',TweetTextSearchView,basename="tweetresarch")
router.register('v5/list/tweet/relation',TweetJoinModelView,basename="tweetrelation")

urlpatterns = [
    path('v2/tweets/list/',TweetListView.as_view(),name="tweetlist"),
    path('v2/tweets/retrieve/',TweetRetrieveView.as_view(),name="tweetritrieve"),
    path('v2/comments/list/',CommentListView.as_view(),name="commentlist"),
    path('v2/comments/retrieve/',CommentRetrieveView.as_view(),name="commentretrieve"),
    path('v4/mytweets/list/',MyTweetProfileView.as_view(),name="mytweets"),
    path('v4/list/get/tweet/',TweetAndUserProfileView.as_view(),name="tweetprofilelists"),
    path('v4/list/get/comment/',CommentAndUserProfileView.as_view(),name="commentprofilelists"),
    path('v4/list/get/retweet/',RetweetAndProfileView.as_view(),name="retweetprofilelists"),
    path('v6/get/tweet/',TweetCommentView.as_view(),name="tweetcomment"),
    path('v7/post/tweet_like',TweetLikeToggleView.as_view(),name="tweetliketoggle"),
    path('v7/post/comment_like',CommentLikeToggleView.as_view(),name="commentliketoggle"),
    path('v7/post/retweet_like',RetweetLikeToggleView.as_view(),name="retweetliketoggle"),
    path('v8/tweet/api',TweetWithUserModelView.as_view(),name="tweetapiview"),
    path('',include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)