from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.expressions import RawSQL
from rest_framework.generics import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions,status
from django.db import connection
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
    
    
class DMRoomListAPIView(APIView):
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
    
    @method_decorator(csrf_protect)
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

class DMRJoinUserListAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    
    def get(self,request,format=None):
        rdata={}
        uid=request.user.id
        try:
            query='''
                select
                    dmp.id,
                    ui.id as user_id,
                    dmr.id as room_id,
                    dmr.room_name,
                    dmr.room_image,
                    dmr.description,
                    dmr.created_on,
                    upi.nickname,
                    upi.account_id
                from
                    dmroom_participation as dmp
                left join
                    dm_room as dmr
                on
                    dmr.id = dmp.dmroom_id
                left join
                    accounts_user as ui
                on
                    dmp.join_user_id = ui.id
                left join
                    user_profile as upi
                on
                    ui.id=upi.user_profile_id
                order by
                    dmr.id asc
                limit 10
                '''
            cursor = connection.cursor()
            cursor.execute(query)
            # dmr_joinuser=cursor.fetchall()
            
            cursor.close()
            rdata["result"] = "success"
            rdata["content"]=dictfetchall(cursor)
            
            return Response(
                data=rdata,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            rdata["result"] = "failture"
            rdata["message"]= "error."
            
            return Response(
                data=rdata,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @method_decorator(csrf_protect)
    def post(self,request,format=None):
        rdata={}
        try:
            input_data=request.data
            uid=request.user.id
            new_join_recode=DMRoomJoinUser.objects.filter(
                join_user=uid,
                dmroom=input_data["id"]
            ).first()
            
            
            if new_join_recode:
                new_join_recode.delete()
                msg = "delete room enter info."
            else:
                new_join=DMRoomJoinUser(
                    join_user=uid,
                    dmroom=input_data["id"]
                )
                new_join.save()
                msg = "created room enter info."
                rdata["result"]="success"
                rdata["message"]=msg
            return Response(
                data=rdata,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            pass

class DMRoomDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request,pk,format=None):
        rdata={}
        try:
            uid=request.user.id
            dmroom=DirectMailRoom.objects.filter(
                create_room_user=uid,
                id=pk
            ).first()
            rdata["result"] = "success"
            rdata["content"]=dmroom
            return Response(
                data=rdata,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            rdata["result"] = "failture"
            rdata["message"]= "error."
            
            return Response(
                data=rdata,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self,request,pk,format=None):
        rdata={}
        try:
            uid=request.user.id
            dmroom_obj=DirectMailRoom.objects.filter(
                id=pk,
                create_room_user=uid
            ).first()
            
            dmroom_serializer=DirectMailRoomSerializer(
                isinstance=dmroom_obj,
                data=request.data,
                partial=True
            )
            dmroom_serializer.is_valid()
            dmroom_serializer.save()
            rdata["result"] = "success"
            rdata["message"]="updated rooms."
            return Response(
                data=rdata,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            
            rdata["result"] = "failture"
            rdata["message"]= "error."
            return Response(
                data=rdata,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DMRJoinUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request,pk,format=None):
        rdata={}
        try:
            uid=request.user.id
            query='''
                select
                    *
                from
                    dmroom_participation as dmp
                left join
                    (
                        select
                            ui.id as user_id,
                            upi.nickname as nn,
                            upi.bio as bio,
                            upi.icon as icon,
                            upi.link as link,
                            upi.account_id as uaid,
                            upi.created_on as join_date
                        from
                            accounts_user as ui
                        left join
                            user_profile as upi
                        on
                            ui.id=upi.user_profile_id
                    ) as ui_tbl
                on
                    dmp.join_user_id = ui_tbl.user_id
                left join
                    dm_room as dmr
                on
                    dmr.id = dmp.dmroom_id
                where
                    dmp.dmroom_id = %s
            '''
            cursor = connection.cursor()
            cursor.execute(query % (pk))
            rdata["result"] = "success"
            rdata["content"]=dictfetchall(cursor)
            return Response(
                data=rdata,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            rdata["result"] = "failture"
            rdata["message"]= "error."
            
            return Response(
                data=rdata,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class DMMessageListAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request,room_id,format=None):
        rdata={}
        
        try:
            uid=request.user.id
            is_join = DMRoomJoinUser.objects.filter(
                join_user=uid,
                dmroom=pk
            )
            
            if is_join is not None:
                query='''
                    select
                        *
                    from
                        dm_message as dmm
                    left join
                        (
                            select
                                ui.id as user_id,
                                upi.nickname as nn,
                                upi.bio as bio,
                                upi.icon as icon,
                                upi.link as link,
                                upi.account_id as uaid,
                                upi.created_on as join_date
                            from
                                accounts_user as ui
                            left join
                                user_profile as upi
                            on
                                ui.id=upi.user_profile_id
                        ) as ui_tbl
                    on
                        dmm.message_user_id = ui_tbl.user_id
                    where
                        dmm.message_user_id = %s
                '''
                cursor = connection.cursor()
                cursor.execute(query % (room_id))
                
                rdata["result"] = "success"
                rdata["content"]=dictfetchall(cursor)
                return Response(
                    data=rdata,
                    status=status.HTTP_200_OK
                )
            else:
                rdata["result"] = "failture"
                rdata["message"]= "error."
                return Response(
                    data=rdata,
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            rdata["result"] = "failture"
            rdata["message"]= "error."
            
            return Response(
                data=rdata,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# class DMMessageDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated,]
    
#     def get(self,request,room_id,format=None):
#         rdata={}
#         try:
            