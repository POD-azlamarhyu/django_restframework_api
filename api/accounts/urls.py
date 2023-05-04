from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import RegisterView,MyUserInfoView,UserModelView,ProfileViewSet,AccountAdminInspectModelView,AccountAdminInspectView,ChannelModelSerializer,MyUserChannelView,ChannelModelView

app_name='accounts'
router = DefaultRouter()
router.register('user/profile',ProfileViewSet)
router.register('account/edit/channel',ChannelModelView)
router.register('account/myuser', UserModelView)


urlpatterns = [
    path('signup/',RegisterView.as_view(),name='registration'),
    path('account/myprofile/',MyUserInfoView.as_view(),name='myprofile'),
    path('account/mychannel/',MyUserChannelView.as_view(),name='mychannel'),
    path('admin/secret/accounts/',AccountAdminInspectModelView.as_view(),name="onlyadminaccounts"),
    path('',include(router.urls))
]
