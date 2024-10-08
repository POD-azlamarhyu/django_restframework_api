from django.test import TestCase
from django.utils import timezone
from accounts.models import *
from django.urls import reverse, resolve
from accounts.views import *

class UserAPIURLTests(TestCase):
    
    
    def test_singup_url(self):
        url = reverse('accounts:registration')
        self.assertEqual(resolve(url).route,'app/api/signup/')
        self.assertEqual(resolve(url).url_name,'registration')
        
    def test_myprofile_url(self):
        url=reverse('accounts:myprofile')
        self.assertEqual(resolve(url).route,'app/api/account/myprofile/')
        
    def test_myuser_url(self):
        url=reverse('accounts:myuser')
        self.assertEqual(resolve(url).route,'app/api/account/myuser/')
        
    def test_user_viewset_url(self):
        url=reverse('accounts:user-list')
        self.assertEqual(resolve(url).func.__name__,UserModelViewSet.__name__)
        self.assertEqual(resolve(url).route,'app/api/account/edit/userinfo/$')
    
    def test_profile_viewset_url(self):
        url=reverse('accounts:userprofile-list')
        self.assertEqual(resolve(url).func.__name__,ProfileViewSet.__name__)
        self.assertEqual(resolve(url).route,'app/api/account/edit/profile/$')