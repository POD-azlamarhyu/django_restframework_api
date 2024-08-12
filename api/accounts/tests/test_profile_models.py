from django.test import TestCase
from django.utils import timezone
from accounts.models import User,UserChannel,UserProfile


class InitialModelTests(TestCase):
    
    def setUp(self) -> None:
        pass
    
    def test_userprofile_is_empty(self):
        getting_model=UserProfile.objects.all()
        self.assertNotEqual(getting_model.count(),1)
    
    def tearDown(self) -> None:
        pass