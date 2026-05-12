import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@gmail.com")

    first_name = "lion"

    last_name = "lion"
