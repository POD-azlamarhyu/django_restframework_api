from rest_framework.test import APIRequestFactory,APITestCase, URLPatternsTestCase,force_authenticate,APIClient
from django.urls import include, path, reverse
from django.test import TestCase
from accounts.models import User,UserChannel,UserProfile
from accounts.factory import UserFactory,ProfileFactory
from rest_framework import status
from apicfg.console import *
from apicfg.utils import *

class JWTViewTest(APITestCase):
    
    def setUp(self):
        user1=User(
            email="tsukiji.not.service@netmeme.com",
            is_active=True,
        )
        user2=User(
            email="ryutaro.nonomura@itmeme.co.jp",
            is_active=True,
        )
        user1.set_password('xn39zksh32a')
        user1.save()
        
        user2.set_password("k39dxmwsks")
        user2.save()
        UserProfile.objects.create(
            nickname="築地市場営業しているニキ＆いないニキ",
            user_profile=user1,
            account_id="tsukiji_market_boy",
            bio="東京の築地市場は営業していません！（営業しております）"
        )
        
        
        UserProfile.objects.create(
            nickname="nonomura ryutaro",
            user_profile=user2,
            account_id="aaaaaaaaa",
            bio="元兵庫県議会所属．俺は゛ね゛ぇ゛デュハハ．おんなじやおんなじや"
        )
        self.user_pw="xn39zksh32a"
        self.user_email="tsukiji.not.service@netmeme.com"
        self.factory=APIRequestFactory()
        self.client=APIClient()
    
    def test_jwt_login(self):
        
        pdata={
            'email':self.user_email,
            'password':self.user_pw
        }
        
        login_url=reverse('token_obtain_pair')
        response=self.client.post(
            login_url,
            pdata,
            format="json"
        )
        
        # response=self.factory
        
        # self.assertTrue("access" in response)
        # self.assertTrue("refresh" in response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_jwt_refresh_token(self):
        
        pdata={
            'email':self.user_email,
            'password':self.user_pw
        }
        
        login_url=reverse('token_obtain_pair')
        login_response=self.client.post(
            login_url,
            pdata,
            format="json"
        )
        
        