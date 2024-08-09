from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.contrib.staticfiles.urls import static
from apicfg import settings
from .views import *

app_name='directmails'
router = DefaultRouter()
router.register('v1/directmail/directmessageroom',DMRoomModelViewSet,basename="dmroomapi")
router.register('v1/directmail/dmroomjointuser',DMRUserModelViewSet,basename="roomjointuser")
router.register('v1/directmail/dmmessage',DMMessageModelViewSet,basename="dmmessage")


urlpatterns=[
    path('',include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)