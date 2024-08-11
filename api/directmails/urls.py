from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.contrib.staticfiles.urls import static
from apicfg import settings
from .views import *

app_name='directmails'
router = DefaultRouter()
router.register('v1/directmail/directmessageroom',DMRoomModelViewSet,basename="dmroomapi")
router.register('v1/directmail/dmroom_joint_user',DMRUserModelViewSet,basename="roomjointuser")
router.register('v1/directmail/dm_message',DMMessageModelViewSet,basename="dmmessage")


urlpatterns=[
    path('v2/directmail/dmroom/list/',DMRoomListAPIView.as_view(),name="dmroomlist"),
    path('v2/directmail/room_joiner/list/',DMRJoinUserListAPIView.as_view(),name="dmroomjoinerlist"),
    path('v2/directmail/dmroom/detail/<int:pk>/',DMRoomDetailAPIView.as_view(),name="dmroomdetail"),
    path('v2/directmail/room_joiner/detail/<int:pk>/',DMRJoinUserDetailAPIView.as_view(),name="dmrjoinuserdetail"),
    path('v2/directmail/message/list/<int:room_id>/',DMMessageListAPIView.as_view(),name="messagelist"),
    path('',include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)