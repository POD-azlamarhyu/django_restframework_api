from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from apicfg import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .views import TweetModelView,CommentModelView,RetweetModelView,TweetListView

app_name='tweets'
router = DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
]