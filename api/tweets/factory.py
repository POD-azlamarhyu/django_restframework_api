import factory
from .models import *
from factory.faker import Faker
from factory.django import DjangoModelFactory
import factory as fty

class TweetFactory(DjangoModelFactory):
    class Meta:
        model = Tweet

    text = Faker("sentence",locale="ja_JP")