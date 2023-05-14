from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.conf import settings
from .models import Tweet,Comment,Retweet
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext


class TweetAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on','update_on')
    fieldsets = (
        (gettext('Tweet Info'),{'fields':('id','user_tweet','text','tweet_img','tweet_like')}),
        (gettext('Tweet Dates'),{'fields':('created_on','update_on',)})
    )

class CommentAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on')
    fieldsets = (
        (gettext('Comment Info'),{'fields':('id','user_comment','tweet','comment_img','comment_like')}),
        (gettext('Comment Dates'),{'fields':('created_on','update_on')})
    )

class RetweetAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on')
    fieldsets = (
        (gettext('Retweet Info'),{'fields':('id','retweet_user','text','user_tweet','retweet_like')}),
        (gettext('Retweet Dates'),{'fields':('created_on',)})
    )

admin.site.register(Tweet,TweetAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Retweet,RetweetAdmin)