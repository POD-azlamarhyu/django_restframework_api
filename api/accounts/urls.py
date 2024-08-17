from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import RegisterView,MyUserProfileView,UserModelViewSet,ProfileViewSet,AccountAdminInspectModelView,AccountAdminInspectView,MyUserChannelView,ChannelModelViewSet,MyUserView,UserProfileView,UserChannelView
from apicfg import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name='accounts'
router = DefaultRouter()
router.register('account/edit/profile',ProfileViewSet)
router.register('account/edit/channelinfo',ChannelModelViewSet)
router.register('account/edit/userinfo', UserModelViewSet)


urlpatterns = [
    path('signup/',RegisterView.as_view(),name='registration'),
    path('account/myuser/',MyUserView.as_view(),name='myuser'),
    path('account/myprofile/',MyUserProfileView.as_view(),name='myprofile'),
    path('account/mychannel/',MyUserChannelView.as_view(),name='mychannel'),
    path('account/user/v1/profile/',UserProfileView.as_view(),name="userprofiles"),
    path('account/user/v1/channel/',UserChannelView.as_view(),name="userprofiles"),
    path('admin/secret/accounts/',AccountAdminInspectModelView.as_view(),name="onlyadminaccounts"),
    path('admin/secret/inspect/',AccountAdminInspectView.as_view(),name="onlyadmininspect"),
    path('',include(router.urls))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)