from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


class DirectMailRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=DirectMailRoom
        fields='__all__'

class DMRoomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=DMRoomJoinUser
        fields='__all__'
        
class DirectMailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMailMessage
        fields='__all__'