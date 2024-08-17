from django.test import TestCase
from django.utils import timezone
from accounts.models import *
from django.urls import reverse, resolve
from accounts.views import *

class UserAPIURLTests(TestCase):
    
    
    def test_singup_url(self):
        url = reverse('accounts:registration')
        self.assertEqual(resolve(url).route,'auth/signup/')
        self.assertEqual(resolve(url).url_name,'registration')
        
    def test_myprofile_url(self):
        url=reverse('accounts:myprofile')
        self.assertEqual(resolve(url).route,'auth/account/myprofile/')
        
    def test_myuser_url(self):
        url=reverse('accounts:myuser')
        self.assertEqual(resolve(url).route,'auth/account/myuser/')
        
    