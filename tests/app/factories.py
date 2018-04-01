from __future__ import unicode_literals
import factory
from tests.app.models import Issue, Office
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

default_password = '1@3$567*9'

class UserFactory(factory.DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = User

    @factory.post_generation
    def define_password(self, created, extracted, **kwargs):
        if created:
            self.set_password(default_password)
            self.save()


class OfficeFactory(factory.DjangoModelFactory):
    name = factory.Faker('bs')
    manager = factory.SubFactory(UserFactory)

    class Meta:
        model = Office


class IssueFactory(factory.DjangoModelFactory):
    description = factory.Faker('text')
    office = factory.SubFactory(OfficeFactory)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Issue