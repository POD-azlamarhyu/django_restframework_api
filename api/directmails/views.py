from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.expressions import RawSQL
from rest_framework.generics import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions,status

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.cache import cache_page
from django.db.models import Q,Prefetch,F,Count,FilteredRelation,Max,Min,Avg,Sum,Subquery,OuterRef,Case,When,Value
from django.http import JsonResponse,Http404
from .models import *
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,BasePermission
from .serializer import *

User = get_user_model()


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns,row))
        for row in cursor.fetchall()
    ]
    

class DMRoomModelViewSet(ModelViewSet):
    queryset=DirectMailRoom.objects.all()
    serializer_class = DirectMailRoomSerializer
    permission_classes = [IsAuthenticated,]
    
class DMRUserModelViewSet(ModelViewSet):
    queryset=DMRoomJoinUser.objects.all()
    serializer_class = DMRoomUserSerializer
    permission_classes = [IsAuthenticated,]
    
class DMMessageModelViewSet(ModelViewSet):
    queryset=DirectMailMessage.objects.all()
    serializer_class=DirectMailMessageSerializer
    permission_classes = [IsAuthenticated,]
    
    
class DMRoomAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request,format=None):
        rdata={}
        try:
            uid=request.user.id
            rooms=DirectMailRoom.objects.filter(create_room_user=uid)
            
            rdata["result"]="success"
            rdata["content"]=rooms
            rdata["message"]="get your created rooms."
            
            return Response(
                data=rdata,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            rdata["result"] = "failture"
            rdata["message"] = "error."
            
            return Response(
                data=rdata,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self,request,format=None):
        rdata={}
        try:
            uid=request.user.id
            input_data=request.data
            
            new_room = DirectMailRoom(
                create_room_user=uid,
                room_name=input_data["room_name"],
                description=input_data["description"],
                room_image=input_data["room_image"],
            )
            saved_obj = new_room.save()
            
            new_roomjoin = DMRoomJoinUser(
                join_user=uid,
                dmroom=saved_obj.pk
            )
            new_roomjoin.save()
            rdata["result"]="success"
            rdata["message"]="created rooms."
            
            return Response(
                data=rdata,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            
            rdata["result"]="faliture"
            rdata["message"]="error."
            
            return Response(
                data=rdata,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )