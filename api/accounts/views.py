from django.shortcuts import render
from rest_framework import permissions,status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView,ListCreateAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,CreateModelMixin
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.cache import cache_page
from .serializer import ProfileSerializer,UserSerializer,ChannelSerializer,UserChangeSerializer,ProfileModelSerializer,ChannelModelSerializer,AccountRelationSerializer,AccountAdminInspectSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse,Http404
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,BasePermission
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from .models import UserProfile,UserChannel
from django.db.models import Q,Prefetch,F
from django.db import connection
from django.forms.models import model_to_dict
import json
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

# Create your views here.

User = get_user_model()


# @csrf_protect
class RegisterView(APIView):
    permission_classes = [AllowAny,]
    
    def post(self,request):
        try:
            data = request.data
            email = data['email']
            password = data['password']
            
            if not User.objects.filter(email=email).exists() and len(password) >= 10:
                User.objects.create_user(
                    email=email,
                    password=password
                )
                return Response(
                    data={'success':'ユーザを作成しました'},
                    status=status.HTTP_201_CREATED
                )
            elif len(password) < 10:
                return Response(
                    data={'error':'パスワードが短いです．10文字以上にしてください'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    data={'error':'このメールアドレスは既に登録されてます'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            return Response(
                data={'error':'問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class MyUserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

class UserModelView(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    # なくていい
    permission_classes=[IsAuthenticated,]

    @action(methods=['get'],detail=True)
    def myaccount(self,request,pk=None):
        queryset = self.get_object()
        if request.user is not None:
            return Response(
                data={
                    'result':'success',
                    'content':{
                        'id':queryset.id,
                        'email':queryset.email,
                        'is_active':queryset.is_active,
                        'joined_date':queryset.joined_date
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(data={
                'result':'error',
                'content':'ユーザ情報がありません'
            },status=status.HTTP_400_BAD_REQUEST)
    @action(methods=['patch'],detail=True)
    def edituseremail(self,request,pk=None):
        user=request.user
        queryset=self.get_object()
        email = request.data['email']
        serializer = UserChangeSerializer(
                data={
                    "email":email,
                },
                partial=True
            )
        
        if serializer.is_valid():
            return Response(
                data={
                    'result':'succsess',
                    'content':serializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'result':'error',
                    'content':serializer.error
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    @action(methods=['patch'],detail=True)
    def edituserpw(self,request,pk=None):
        queryset=self.get_object()
        password = request.data['password']
        serializer = UserChangeSerializer(
                data={
                    "password":password,
                },
                partial=True
            )
        
        if serializer.is_valid():
            return Response(
                data={
                    'result':'succsess',
                    'content':serializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'result':'error',
                    'content':serializer.error
                },
                status=status.HTTP_400_BAD_REQUEST
            )
class UserProfileView(APIView):
    permission_classes = [AllowAny,]
    
    def get(self,request,format=None):
        res={}
        try:
            
            accounts = UserProfile.objects.select_related('user_profile').get(user_profile_id="6ee49e44-e22f-49a7-bccb-5b2533a04bb9")
            
            # res["id"]=accounts.id
            # res["nickname"]=accounts.nickname
            # res["created_on"]=accounts.created_on
            # res["update_at"]=accounts.update_at
            # res["account_id"]=accounts.account_id
            # res["bio"]= accounts.bio

            # if accounts.icon is not None:
            #     res["icon"]=accounts.icon.path
            # else:
            #     res["icon"]=""
                
            # res["link"]=accounts.link
            # user_profile = {}
            # user_profile["id"]=accounts.user_profile.id
            # user_profile["email"]=accounts.user_profile.email
            # user_profile["last_login"]=accounts.user_profile.last_login
            # user_profile["is_staff"]=accounts.user_profile.is_staff
            # user_profile["is_superuser"]=accounts.user_profile.is_superuser
            # res["user_profile"]=user_profile
            serializer = ProfileModelSerializer(accounts)
            return Response(
                data={
                    "result":"success",
                    "content":serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                data={
                    "result":"error",
                    "content":"問題が発生"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class UserChannelView(APIView):
    permission_classes = [AllowAny,]
    
    def get(self,request,format=None):
        
        try:
            # query = UserChannel.objects.select_related("user_channel").get(user_channel_id=request.user.id)
            query = UserChannel.objects.select_related("user_channel").get(user_channel_id="6ee49e44-e22f-49a7-bccb-5b2533a04bb9")
            serializer = ChannelModelSerializer(query)
            return Response(
                data={
                    "result":"success",
                    "content":serializer.data
                },
                status=status.HTTP_200_OK
            )
        except UserChannel.DoesNotExist:
            return Response(
                data={
                    "result":"success",
                    "content":"None"
                },
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(
                data={
                    "result":"success",
                    "content":"None"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                data={
                    "result":"error",
                    "content":"問題が発生"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def post(self,request,format=None):
        try:
            query = UserChannel(
                channel_id=request.data["channel_id"],
                user_channel=request.data["user_channel"],
                channel_icon= request.data["channel_icon"],
                channel_cover=request.data["channel_cover"]
            )
            query.save()
            # serializer = ChannelModelSerializer(data=request.data)
            
            # serializer.is_valid()
            # serializer.save()
            return Response(
                data={
                    "result":"success",
                    "content":"投稿しました"
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(e)
            return Response(
                data={
                    "result":"error",
                    "content":"問題が発生"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class ChannelModelView(viewsets.ModelViewSet):
    queryset = UserChannel.objects.all()
    serializer_class = ChannelSerializer
    
    def perform_create(self,serizalizer):
        serizalizer.save(user_channel=self.request.user)
class MyUserChannelView(ListCreateAPIView):
    queryset = UserChannel.objects.all()
    serializer_class = ChannelSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
class AccountAdminInspectModelView(
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
):
    queryset=User.objects.all()
    serializer_class=AccountAdminInspectSerializer
    def get_queryset(self):
        return self.queryset.all()
    
    def list(self,request):
        queryset=self.get_queryset
        serializer=AccountAdminInspectSerializer(queryset,many=True)
        
        return Response(serializer.data)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        return Response(
            data={
                'result':'success'
            },
            status=status.HTTP_201_CREATED
        )

class DistributeIsAdminPermission(BasePermission):
    def has_permission(self,request,view):
        
        return request.user and request.user.is_superuser == True
class AccountAdminInspectView(APIView):
    permission_classes = [DistributeIsAdminPermission,]
    
    def get(self,request,format=None):
        # Inner join
        sql_query = '''
            select 
                *
            from
                accounts_user as ui
            left join
                accounts_userprofile as upi
            on
                ui.id = upi.user_profile_id
            left join
                accounts_userchannel as uci
            on 
                ui.id=uci.user_channel_id
        '''
        cursor = connection.cursor()
        cursor.execute(sql_query)
        accounts = cursor.fetchall()

        return Response(
            data={
                "result":"success",
                "content":list(accounts)
            },
            status=status.HTTP_200_OK
        )
    

class MyUserProfileView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user_profile=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    
    def perform_create(self,serizalizer):
        serizalizer.save(user_profile=self.request.user)


