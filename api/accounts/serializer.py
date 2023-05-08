from dataclasses import field
from pyexpat import model
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserChannel,UserProfile
User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'nickname',
            'user_profile',
            'account_id',
            'bio',
            'icon',
            'link',
            'created_on',
            'update_at',
        )
        read_only_fields = ['id','user_profile']
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=('id','email','is_staff','joined_date','is_superuser')
        read_only_fields = ['id',]
        extra_kwargs = {
            'password': {'write_only': True},
        }
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChannel
        fields=('id','user_channel','channel_name','channel_icon','channel_cover')
        read_only_fields = ['id','user_channel']
        
class UserChangeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=('id','email','password','is_staff','joined_date','is_superuser')
        read_only_fields = ['id',]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def create(self,validated_data):
        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        else:
            instance=super().update(instance,validated_data)
        return instance


class ProfileModelSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    update_at = serializers.DateTimeField(format="%Y-%m-%d",read_only=True)
    user_profile=UserSerializer(read_only=True)
    class Meta:
        model=UserProfile
        fields=('id','nickname','user_profile','user_profile_id','account_id','bio','icon','link','created_on','update_at')


class ChannelModelSerializer(serializers.ModelSerializer):
    user_channel=UserSerializer(read_only=True)
    class Meta:
        model=UserChannel
        fields=('id','channel_name','user_channel','user_channel_id','account','channel_icon','channel_cover')

class AccountRelationSerializer(serializers.ModelSerializer):
    profile=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    channel=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    class Meta:
        model=User
        fields=('id','email','is_staff','joined_date','profile','channel')
        read_only_fields = ['id',]
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
class AccountAdminInspectSerializer(serializers.ModelSerializer):
    profile=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    channel=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    class Meta:
        model=User
        fields=('id','email','password','is_staff','joined_date','profile','channel')
        read_only_fields = ['id',]
        