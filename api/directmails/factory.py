from .models import *
from factory.faker import Faker
from factory.django import DjangoModelFactory,ImageField
import factory
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class DMroomFactory(DjangoModelFactory):
    class Meta:
        model = DirectMailRoom
    
    room_name=Faker(
        "word",
        locale="en_US"
    )
    description=Faker(
        "sentence",
        locale="ja_JP"
    )
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    updated_on= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    @factory.lazy_attribute
    def create_room_user(self):
        array = [1,2,1,1,1,1,1,2,2,2,2,1,1,1,2,2,1,1,1,]
        if random.choice(array) == 1:
            user=User.objects.filter(is_staff=True).first()
        else:
            user=User.objects.filter(is_staff=False).first()
        
        return user


class DMroomUserFactory(DjangoModelFactory):
    class Meta:
        model = DMRoomJoinUser
    
    @factory.lazy_attribute
    def join_user(self):
        array = [1,2,1,1,1,1,1,2,2,2,2,1,1,1,2,2,1,1,1,1,1,1,1,1]
        if random.choice(array) == 1:
            user=User.objects.filter(is_staff=True).first()
        else:
            user=User.objects.filter(is_staff=False).first()
        
        return user
    
    @factory.lazy_attribute
    def dmroom(self):

        room_id = DirectMailRoom.objects.all().order_by('?').first()
        return room_id
    
class DMMessageFactory(DjangoModelFactory):
    class Meta:
        model = DirectMailMessage
    
    message=Faker(
        "sentence",
        locale="ja_JP"
    )
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    updated_on= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    @factory.lazy_attribute
    def message_user(self):
        array = [1,2,1,1,1,1,1,2,2,2,2,1,1,1,2,2,1,1,1,1,1,1,1,1]
        if random.choice(array) == 1:
            user=User.objects.filter(is_staff=True).first()
        else:
            user=User.objects.filter(is_staff=False).first()
        
        return user
    
    @factory.lazy_attribute
    def dm_room(self):

        room_id = DirectMailRoom.objects.all().order_by('?').first()
        return room_id
