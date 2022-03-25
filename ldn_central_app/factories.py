import factory
from django.contrib.auth.models import User

from . import models


class GymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Gym

    name = factory.Faker("company")
    gym_details = factory.Faker("paragraph")
    gym_link = factory.Faker("url")
    description = factory.Faker("paragraph")
    quality = factory.Faker("paragraph")
    access = factory.Faker("paragraph")
    network = factory.Faker("paragraph")
    contract = factory.Faker("paragraph")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("word")
    email = factory.Faker("email")
    is_active = True
    password = factory.PostGenerationMethodCall("set_password", "password123")
