from django.db import models
import factory
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
import random
from django.utils import timezone
import string
# Create your models here.
User = get_user_model()

def return_room_id():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(15))
    return random_string

def return_room_image_path(instance,filename):
    ext = filename.split('.')[-1]
    return '/'.join(['dmroom',str(instance.id).zfill(5),str(instance.room_id).zfill(10)+str(instance.created_on)+str(".")+str(ext)])

def return_message_image_path(instance,filename):
    ext = filename.split('.')[-1]
    return '/'.join(['message','image',str(instance.id).zfill(5),str(instance.message_user.id).zfill(10)+str(instance.created_on)+str(".")+str(ext)])

def return_message_video_path(instance,filename):
    ext = filename.split('.')[-1]
    return '/'.join(['message','video',str(instance.id).zfill(5),str(instance.message_user.id).zfill(10)+str(instance.created_on)+str(".")+str(ext)])

class DirectMailRoom(models.Model):
    room_id=models.TextField(
        verbose_name="room id",
        max_length=15,
        unique=True,
        default=return_room_id,
        editable=False
    )
    create_room_user=models.ForeignKey(
        User,
        related_name="create_user_id",
        on_delete=models.SET_NULL,
        null=True
    )
    room_name=models.TextField(
        verbose_name="room name",
        default="directmail room",
        max_length=50,
        unique=False,
        blank=True,
        null=True
    )
    room_image=models.ImageField(
        verbose_name="room image",
        blank=True,
        null=True,
        upload_to=return_room_image_path,
    )
    description=models.TextField(
        verbose_name="description",
        blank=True,
        null=True,
        max_length=255,
    )
    created_on=models.DateTimeField(
        verbose_name="created date",
        default=timezone.now,
        null=True,
        editable=False
    )
    updated_on=models.DateTimeField(
        verbose_name="updated date",
        default=timezone.now,
        null=True
    )
    
    class Meta:
        db_table="dm_room"
    
    def __str__(self) -> str:
        if self.room_name is None:
            return f'{self.id} : {self.room_id}'
        else:
            return f'{self.pk} : {self.room_name}'
class DMRoomJoinUser(models.Model):
    join_user = models.ForeignKey(
        User,
        related_name="join_user_id",
        on_delete=models.CASCADE,
    )
    dmroom = models.ForeignKey(
        DirectMailRoom,
        related_name="dm_room_id",
        on_delete=models.CASCADE
    )
    created_on=models.DateTimeField(
        verbose_name="created date",
        default=timezone.now,
        null=True,
    )
    
    class Meta:
        db_table="dmroom_participation"
class DirectMailMessage(models.Model):
    
    message_user=models.ForeignKey(
        User,
        related_name="message_user_id",
        on_delete= models.CASCADE
    )
    message=models.TextField(
        verbose_name="message text",
        blank=True,
        max_length=500
    )
    dm_room=models.ForeignKey(
        DirectMailRoom,
        related_name="message_room_id",
        on_delete=models.CASCADE
    )
    image=models.ImageField(
        verbose_name="dm image",
        blank=True,
        null=True,
        upload_to=return_message_image_path
    )
    video=models.FileField(
        verbose_name="dm video",
        blank=True,
        null=True,
        upload_to=return_message_video_path
    )
    created_on=models.DateTimeField(
        verbose_name="created date",
        default=timezone.now,
        null=True,
        editable=False
    )
    updated_on=models.DateTimeField(
        verbose_name="updated date",
        default=timezone.now,
        null=True
    )
    class Meta:
        db_table="dm_message"
    
    def __str__(self) -> str:
        return f'{self.id} : {self.message_user}'
        