from django.shortcuts import render
from rest_framework import permissions,status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,CreateModelMixin
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.cache import cache_page
from .serializer import ProfileSerializer,UserSerializer,ChannelSerializer,UserChangeSerializer,ProfileModelSerializer,ChannelModelSerializer,AccountRelationSerializer,AccountAdminInspectSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse,Http404
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from .models import UserProfile,UserChannel
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
class UserModelView(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    # なくていい
    permission_classes=[IsAuthenticated]
    
    @action(methods=['get'],detail=True)
    def myaccount(self,request):
        
        if request.user is not None:
            return Response(
                data={
                    'result':'success',
                    'content':{
                        'email':request.user.email,
                        'is_active':request.user.is_active,
                        'joined_date':request.user.email
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(data={
                'result':'error',
                'content':'ユーザ情報がありません'
            }
            )
    @action(methods=['put','patch'],detail=True)
    def user_registration(self,request):
        user=request.user
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
class ChannelModelView(viewsets.ModelViewSet):
    queryset = UserChannel.objects.all()
    serializer_class = ChannelSerializer
    
    def perform_create(self,serizalizer):
        serizalizer.save(user_channel=self.request.user)

class MyUserChannelView(RetrieveUpdateDestroyAPIView):
    queryset = UserChannel.objects.all()
    serializer_class = ChannelSerializer
    
class AccountAdminInspectModelView(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericAPIView
):
    queryset=User.objects.all()
    serializer_class=AccountAdminInspectSerializer
    
    def list(self,request):
        queryset=queryset
        serializer=AccountAdminInspectSerializer(queryset,many=True)
        
        return Response(serializer.data)
class AccountAdminInspectView(APIView):
    authentication_classes = []
    permission_classes = [IsAdminUser,]
    def get(self,request,pk,format=None):
        pass


class MyUserInfoView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user_profile=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    
    def perform_create(self,serizalizer):
        serizalizer.save(user_profile=self.request.user)


