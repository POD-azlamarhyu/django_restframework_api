from rest_framework.test import APIRequestFactory,APITestCase, URLPatternsTestCase,force_authenticate,APIClient
from django.urls import include, path, reverse
from django.test import TestCase
from accounts.models import User,UserChannel,UserProfile
from accounts.factory import UserFactory,ProfileFactory
from rest_framework import status
from apicfg.console import *
from apicfg.utils import *

class JWTViewTest(APITestCase,TestCase):
    
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
        
        self.userPw="k39dxmwsks"
        self.userEmail="ryutaro.nonomura@itmeme.co.jp"
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
        
        login_res_data=login_response.data
        self.assertEqual(login_response.status_code,status.HTTP_200_OK)
        
        refresh_url=reverse('token_refresh')
        # debug_list_pprint(login_res_data["access"])
        # debug_list_pprint(login_res_data["refresh"])
        pdata={
            "refresh":login_res_data["refresh"]
        }
        refresh_response=self.client.post(
            refresh_url,
            pdata,
            format="json"
        )
        
        refresh_data=refresh_response.data
        
        self.assertEqual(refresh_response.status_code,status.HTTP_200_OK)
        self.assertTrue("access" in refresh_data)
    
    def test_jwt_verify_token(self):
        
        # pdata={
        #     'email':self.user_email,
        #     'password':self.user_pw
        # }
        pdata={
            'email':self.userEmail,
            'password':self.userPw
        }
        
        login_url=reverse('token_obtain_pair')
        login_response=self.client.post(
            login_url,
            pdata,
            format="json"
        )
        
        login_res_data=login_response.data
        self.assertEqual(login_response.status_code,status.HTTP_200_OK)
        
        verify_url=reverse('token_verify')
        pdata={
            "token":login_res_data["access"]
        }
        # self.client.credentials(
        #     HTTP_AUTHORIZATION=f'JWT {login_res_data["access"]}'
        # )
        verify_response=self.client.post(
            verify_url,
            pdata,
            format="json"
        )
        
        self.assertEqual(verify_response.status_code,status.HTTP_200_OK)
    
    def test_jwt_logout(self):
        # pdata={
        #     'email':self.user_email,
        #     'password':self.user_pw
        # }
        pdata={
            'email':self.userEmail,
            'password':self.userPw
        }
        
        login_url=reverse('token_obtain_pair')
        login_response=self.client.post(
            login_url,
            pdata,
            format="json"
        )
        
        login_res_data=login_response.data
        self.assertEqual(login_response.status_code,status.HTTP_200_OK)
        
        logout_url=reverse('token_blacklist')
        pdata={
            "refresh":login_res_data["refresh"]
        }
        logout_response=self.client.post(
            logout_url,
            pdata,
            format="json"
        )
        self.assertEqual(logout_response.status_code,status.HTTP_200_OK)
    