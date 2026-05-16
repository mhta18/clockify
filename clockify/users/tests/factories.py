import factory
import random
from users.models import User
from django.utils import timezone

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Generates unique emails sequentially: user1@gmail.com, user2@gmail.com...
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")

    # Generates realistic random first and last names
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    # Generates a random phone number string
    phone_number = factory.Faker("numerify", text="##########")

    # Cycle randomly through your exact GENDER_CHOICES ('male', 'female', 'other')
    gender = factory.Iterator(
        [choice[0] for choice in User.GENDER_CHOICES],
        getter=lambda c: random.choice([choice[0] for choice in User.GENDER_CHOICES]),
    )

    # Generates a random birth date (e.g., between ages 18 and 65)
    birth_date = factory.Faker("date_of_birth", minimum_age=10, maximum_age=65)

    # Generates a random country name
    country = factory.Faker("country")

    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    # Defaults for status flags (can still be overridden manually in tests)
    is_active = True
    is_staff = False
    is_admin = False

