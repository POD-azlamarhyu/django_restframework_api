from django.test import TestCase
from django.utils import timezone
from accounts.models import User,UserChannel,UserProfile


class InitialModelTests(TestCase):
    
    def setUp(self) -> None:
        pass
        
    
    def test_user_model_is_empty(self):
        
        getting_model=User.objects.all()
        
        self.assertEqual(getting_model.count(),0)
        self.assertNotEqual(getting_model.count(),2)
        
    def test_is_posted_data(self):
        new_user=User(
            email="example.example@example.co.jp",
            password="aks93ks9xke"
        )
        new_user.save()
        
        user=User.objects.all()
        
        self.assertEqual(user.count(),1)
        self.assertNotEqual(user.count(),0)
        
class UserModelTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email="unko.unko@example.jp",
            password="xn39zksh32a"
        )
        User.objects.create_user(
            email="manko.1919@example.jp",
            password="k39dxmwsks"
        )
    
    def test_post_data_success(self):
        User.objects.create_user(
            email="chinko.chinko@email.us",
            password="zb38s9zkf"
        )
        
        save_user=User.objects.all()
        self.assertEqual(save_user.count(),3)
        self.assertNotEqual(save_user.count(),2)

    def test_normal_user_count(self):
        
        new_user=User(
            email="example.example@example.co.jp",
            password="aks93ks9xke"
        )
        
        new_user.save()
        
        normal_user=User.objects.filter(
            is_superuser=False,
            is_staff=False
        )
        
        self.assertEqual(normal_user.count(),3)
    
    def test_superuser_create(self):
        new_super_user=User(
            email="superunko.unko@example.jp",
            password="znv93kxlabe",
            is_superuser=True,
            is_staff=True,
        )
        
        new_super_user.save()
        
        super_user=User.objects.filter(
            is_superuser=True,
            is_staff=True
        )
        self.assertEqual(super_user.count(),1)
    
    def test_confirm_create_user(self):
        new_user=User(
            email="manko.unko@example.jp",
            password="zkkk93kxlabe",
        )
        
        new_user.save()
        
        saved_user=User.objects.get(email="manko.unko@example.jp")
        self.assertEqual(saved_user,new_user)
    
    def test_confirm_create_suser(self):
        new_user=User(
            email="superunko.unko@example.jp",
            password="znv93kxlabe",
            is_superuser=True,
            is_staff=True,
        )
        
        new_user.save()
        
        saved_user=User.objects.get(email="superunko.unko@example.jp")
        
        self.assertEqual(saved_user,new_user)
    

    def test_get_user(self):
        
        users=User.objects.all()
        self.assertEqual(users.count(),2)
    
    def test_post_get_user(self):
        data=[
            {
                "email":"gomi.of.gomi@example.us",
                "pw":"uzk39xb20a"
            },
            {
                "email":"gomi.of.chinko@example.uk",
                "pw":"uzxzve2az"
            },
        ]
        
        nusers=[]
        for i,d in enumerate(data):
            new_user=User(
                email=d["email"],
                password=d["pw"]
            )
            nusers.append(new_user)
            
        suuser=User.objects.bulk_create(nusers)
        
        save_users=User.objects.all()
        self.assertEqual(save_users.count(),4)
        
        self.assertEqual(User.objects.filter(email=data[0]["email"]).exists(),True)
        
        self.assertNotEqual(User.objects.filter(email=data[1]["email"]).exists(),False)
    
    def test_update_email_user(self):
        new_user= User(
            email="chinko.chinko@email.us",
            password="zb38s9zkf"
        )
        
        new_user.save()
        
        update_user=User.objects.filter(
            email=new_user.email
        ).first()
        
        update_user.email="gomi.unko.chinko@example.jp"
        update_user.save()
        
        self.assertNotEqual(update_user.email,new_user.email)

    def test_update_and_before_user(self):
        new_user= User(
            email="chinko.manko@email.au",
            password="zb38s9zkf"
        )
        
        new_user.save()
        saved_user=User.objects.filter(
            email=new_user.email
        ).first()
        
        saved_user_id=saved_user.id
        saved_user_email=saved_user.email
        
        update_user=saved_user
        
        update_user.email="gomi.unko.chinko@example.jp"
        update_user.save()
        
        updated_user=User.objects.filter(
            id=saved_user.id
        ).first()
        
        updated_user_id=updated_user.id
        updated_user_email=updated_user.email
        
        self.assertEqual(saved_user,update_user)
        self.assertEqual(saved_user_id,updated_user_id)
        self.assertNotEqual(saved_user_email,updated_user_email)
        
    def test_delete_user_count(self):
        new_user= User(
            email="chinko.manko@email.au",
            password="zb38s9zkf"
        )
        
        new_user.save()
        
        before_users=User.objects.all().count()
        
        del_user=User.objects.order_by('?').first()
        del_user.delete()
        
        after_users=User.objects.all().count()
        
        self.assertNotEqual(before_users,after_users)