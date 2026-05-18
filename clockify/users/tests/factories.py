import factory
import random
from users.models import User
from django.utils import timezone

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    phone_number = factory.Faker("numerify", text="##########")

    gender = factory.Iterator(
        [choice[0] for choice in User.GENDER_CHOICES],
        getter=lambda c: random.choice([choice[0] for choice in User.GENDER_CHOICES]),
    )

    birth_date = factory.Faker("date_of_birth", minimum_age=10, maximum_age=65)

    country = factory.Faker("country")

    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    is_active = True
    is_staff = False
    is_admin = False

