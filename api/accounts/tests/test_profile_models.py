from django.test import TestCase
from django.utils import timezone
from accounts.models import User,UserChannel,UserProfile
from accounts.factory import UserFactory,ProfileFactory


class InitialModelTests(TestCase):
    
    def setUp(self) -> None:
        pass
    
    def test_userprofile_is_empty(self):
        getting_model=UserProfile.objects.all()
        self.assertNotEqual(getting_model.count(),1)
    
    def tearDown(self) -> None:
        pass
    
class UserProfileModelTests(TestCase):
    def setUp(self) -> None:
        self.user1=User.objects.get(email="tsukiji.not.service@netmeme.com")
        self.user2=User.objects.get(email="ryutaro.nonomura@itmeme.co.jp")
        
    
    @classmethod
    def setUpTestData(cls) -> None:
        user1=User(
            email="tsukiji.not.service@netmeme.com",
        )
        user2=User(
            email="ryutaro.nonomura@itmeme.co.jp",
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
            bio="俺は゛ね゛ぇ゛デュハハ．おんなじやおんなじや"
        )
        
        return super().setUpTestData()

    def test_post_user_and_profile_count(self):
        new_user=User(
            email="society.dont.allow@itmeme.co.jp"
        )
        new_user.set_password("vzhksfjke")
        new_user.save()
        UserProfile.objects.create(
            nickname="akihabara 社会は許してくれいないニキ",
            user_profile=new_user,
            account_id="society",
            bio="それは，世間は許してくれないよねぇ．ああああああああああああいいいいいいいいいいいいいいいい"
        )
        
        saved_user_model=User.objects.all()
        saved_pro_model=UserProfile.objects.all()
        
        self.assertEqual(saved_user_model.count(),3)
        self.assertEqual(saved_pro_model.count(),3)
    
    def test_post_user_and_profile(self):
        new_user=User(
            email="society.dont.allow@itmeme.co.jp"
        )
        new_user.set_password("vzhksfjke")
        new_user.save()
        UserProfile.objects.create(
            nickname="akihabara 社会は許してくれいないニキ",
            user_profile=new_user,
            account_id="society",
            bio="それは，世間は許してくれないよねぇ．ああああああああああああいいいいいいいいいいいいいいいい"
        )
        
        saved_user_model=User.objects.get(email=new_user.email)
        saved_pro_model=UserProfile.objects.get(user_profile=new_user)
        
        self.assertEqual(saved_user_model,new_user)
        self.assertEqual(saved_pro_model.account_id,"society")
        self.assertEqual(saved_pro_model.bio,"それは，世間は許してくれないよねぇ．ああああああああああああいいいいいいいいいいいいいいいい")
        self.assertEqual(saved_pro_model.user_profile,saved_user_model)
        
        
    def test_update_profile(self):
        profile=UserProfile.objects.get(user_profile=self.user2)
        before_user_accountid=profile.account_id
        before_user_nickname=profile.nickname
        before_user_bio=profile.bio
        before_user_icon=profile.icon
        before_user_created=profile.created_on
        before_user=profile.user_profile.pk
        
        profile.account_id="orehane!! deyuhaha"
        profile.bio="俺は゛ね゛ぇ゛デュハハ．おんなじやおんなじやとおもて！！あなたにはわからないでしょうね！！"
        profile.save()
        
        after_user=UserProfile.objects.get(user_profile=self.user2)
        
        self.assertEqual(before_user,after_user.user_profile.pk)
        self.assertEqual(before_user_nickname,after_user.nickname)
        self.assertNotEqual(before_user_accountid,after_user.account_id)
        self.assertNotEqual(before_user_bio,after_user.bio)
        self.assertEqual(before_user_icon,after_user.icon)
        self.assertEqual(before_user_created,after_user.created_on)