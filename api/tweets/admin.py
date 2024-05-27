from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.conf import settings
from .models import Tweet,Comment,Retweet,TweetLikeTBL,CommentLikeTBL,RetweetLikeTBL
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext


class TweetAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on','update_on')
    fieldsets = (
        (gettext('Tweet Info'),{'fields':('id','tweet_user','text','tweet_img')}),
        (gettext('Important dates'),{'fields':('created_on','update_on',)})
    )
    search_fields = ("id","tweet_user","text","created_on")
    list_display = ("id", "tweet_user","created_on",'tweet_img')

class CommentAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on')
    fieldsets = (
        (gettext('Comment Info'),{'fields':('id','comment_user','tweet','comment_img')}),
        (gettext('Important dates'),{'fields':('created_on','update_on')})
    )
    search_fields = ("id","comment_user","text","created_on")
    # list_filter = ("id","tweet_user","tweet_like","created_on")
    list_display = ("id", "comment_user","text", "created_on",'comment_img')


class RetweetAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on')
    fieldsets = (
        (gettext('Retweet Info'),{'fields':('id','retweet_user','text','tweet')}),
        (gettext('Important dates'),{'fields':('created_on',)})
    )
    search_fields = ("id","retweet_user","text","created_on")
    # list_filter = ("id","tweet_user","tweet_like","created_on")
    list_display = ("id", "retweet_user","text", "created_on")



admin.site.register(Tweet,TweetAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Retweet,RetweetAdmin)
admin.site.register(TweetLikeTBL)
admin.site.register(CommentLikeTBL)
admin.site.register(RetweetLikeTBL)