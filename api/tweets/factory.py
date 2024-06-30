from .models import *
from factory.faker import Faker
from factory.django import DjangoModelFactory,ImageField
import factory
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class TweetFactory(DjangoModelFactory):
    class Meta:
        model = Tweet

    text = Faker("sentence",nb_words=30,locale="ja_JP")
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    update_on= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    tweet_img=ImageField(color='blue')
    
    @factory.lazy_attribute
    def tweet_user(self):
        array = [1,2,1,1,1,1,1,2,2,2,2,1,1,1,2,2,1,1,1,]
        if random.choice(array) == 1:
            user=User.objects.filter(is_staff=True).first()
        else:
            user=User.objects.filter(is_staff=False).first()
            
        
        return user

class TweetAllUserFactory(DjangoModelFactory):
    class Meta:
        model = Tweet

    text = Faker("sentence",locale="ja_JP")
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    update_on= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    @factory.lazy_attribute
    def tweet_user(self):
        
        user=User.objects.all().order_by('?').first()
        return user

class TweetStaffUserFactory(DjangoModelFactory):
    class Meta:
        model = Tweet

    text = Faker("paragraph",locale="ja_JP")
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    update_on= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    @factory.lazy_attribute
    def tweet_user(self):
        
        user=User.objects.filter(is_staff=True).order_by('?').first()
        return user

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
    text = Faker("paragraph",locale="ja_JP")
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    update_on= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    
    @factory.lazy_attribute
    def comment_user(self):
        user=User.objects.all().order_by('?').first()
        return user
    
    @factory.lazy_attribute
    def tweet(self):
        admin_users = User.objects.filter(is_staff=True).values_list("id",flat=True)
        uuid_list=[str(col) for col in admin_users]
        tweet_id = Tweet.objects.filter(tweet_user__in=uuid_list).order_by('?').first()
        return tweet_id

class ReTweetFactory(DjangoModelFactory):
    class Meta:
        model=Retweet
        
    text = Faker("paragraph",locale="ja_JP")
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    update_on= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    @factory.lazy_attribute
    def retweet_user(self):
        user=User.objects.all().order_by('?').first()
        return user
    
    @factory.lazy_attribute
    def tweet(self):
        admin_users = User.objects.filter(is_staff=True).values_list("id",flat=True)
        uuid_list=[str(col) for col in admin_users]
        tweet_id = Tweet.objects.filter(tweet_user__in=uuid_list).order_by('?').first()
        return tweet_id
    
    
class TweetLikeTBLFactory(DjangoModelFactory):
    class Meta:
        model = TweetLikeTBL
        django_get_or_create=(('tweet_like_user','tweet'))
    
    @factory.lazy_attribute
    def tweet_like_user(self):
        user=User.objects.all().order_by('?').first()
        return user
    
    @factory.lazy_attribute
    def tweet(self):
        admin_users = User.objects.filter(is_staff=True).values_list("id",flat=True)
        uuid_list=[str(col) for col in admin_users]
        tweet_id = Tweet.objects.filter(tweet_user__in=uuid_list).order_by('?').first()
        return tweet_id
    
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )