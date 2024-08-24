from rest_framework.test import APIRequestFactory,APITestCase, URLPatternsTestCase,force_authenticate,APIClient
from django.urls import include, path, reverse
from django.test import TestCase
from accounts.models import User,UserChannel,UserProfile
from accounts.factory import UserFactory,ProfileFactory
from rest_framework import status
from apicfg.console import *
from apicfg.utils import *

class UserModelViewTest(APITestCase,TestCase):
    
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
        self.login_res_data=login_response.data
        self.access_token=self.login_res_data["access"]
        self.access_refresh=self.login_res_data["refresh"]
    
    def test_view_user_post(self):
        user_email="atama.warukunaika@netmeme.com"
        user_pw="bz39xfa%jfbs"
        
        pdata={
            'email':user_email,
            'password':user_pw
        }
        
        url=reverse("accounts:registration")
        response=self.client.post(
            url,
            pdata,
            format="json"
        )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data,{'success':'ユーザを作成しました'})
        
    
    def test_get_user_info(self):
        url=reverse('accounts:myuser')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.access_token}'
        )
        response=self.client.get(
            url,
            format="json"
        )
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_view_get_user(self):
        url=reverse('accounts:user-list')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.access_token}'
        )
        response=self.client.get(
            url,
            format="json"
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
class UserModelExceptionTest(APITestCase,TestCase):
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
        self.login_res_data=login_response.data
        self.access_token=self.login_res_data["access"]
        self.access_refresh=self.login_res_data["refresh"]
    
    def test_user_post_email_none(self):
        user_email="atama.warukunaika@netmeme.com"
        user_pw="bz39xfa%jfbs"
        
        pdata={
            'password':user_pw
        }
        
        url=reverse("accounts:registration")
        response=self.client.post(
            url,
            pdata,
            format="json"
        )
        self.assertEqual(response.status_code,status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def test_user_post_email_exists(self):
        user_email="atama.warukunaika@netmeme.com"
        user_pw="bz39xfa%jfbs"
        
        pdata={
            'email':self.user_email,
            'password':user_pw
        }
        
        url=reverse("accounts:registration")
        response=self.client.post(
            url,
            pdata,
            format="json"
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,{'error':'このメールアドレスは既に登録されてます'})
    
    def test_get_userinfo_unauth(self):
        url=reverse('accounts:myuser')
        
        response=self.client.get(
            url,
            format="json"
        )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)