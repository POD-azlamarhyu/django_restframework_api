import factory
from .models import *
from factory import Faker,PostGenerationMethodCall,Sequence,SubFactory,RelatedFactory
from factory.django import DjangoModelFactory
import factory as fty
from datetime import datetime, timedelta



class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create=('email',)
    
    # id = Faker("uuid4")
    email = Faker("email",locale='ja_JP')
    password=PostGenerationMethodCall("set_password","password")
    joined_date = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )

class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create=('user_profile','account_id')
    
    nickname = Faker("name",locale='ja_JP')
    user_profile=SubFactory(UserFactory)
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    update_at= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    account_id = Sequence(lambda n: 'account_id_000%d' % n)
    bio = Faker("paragraph",locale='ja_JP')
    
class ProfileCreatedFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile
    
    nickname = Faker("name",locale='ja_JP')
    
    created_on = Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    update_at= Faker(
        "date_between_dates",
        date_start=(datetime.now() - timedelta(days=1000)).date(),
        date_end=datetime.now(),
    )
    account_id = Sequence(lambda n: 'account_id010%d' % n)
    bio = Faker("paragraph",locale='ja_JP')

    @factory.lazy_attribute
    def user_profile(self):
        profiles=UserProfile.objects.values_list("user_profile",flat=True)
        uuid_list= [str(col) for col in profiles]
        users = User.objects.exclude(id__in=uuid_list).order_by('?').first()
        return users