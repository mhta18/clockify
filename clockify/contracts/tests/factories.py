import factory
from contracts.models import Contract, FreelancerContract, EmployerContract
from users.tests.factories import UserFactory
from datetime import date, timedelta


class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract
        abstract = True

    user = factory.SubFactory(UserFactory)

    role_title = factory.Faker("job")
    start_date = factory.LazyFunction(date.today)
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=20))


class FreelancerContractFactory(ContractFactory):
    class Meta:
        model = FreelancerContract

    hourly_payment = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=2000,
        max_value=6000,
    )
    daily_hours_required = factory.Faker("random_int", min=4, max=9)
    document_file = None


class EmployerContractFactory(ContractFactory):
    class Meta:
        model = EmployerContract

    monthly_payment = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=3,
        positive=True,
        min_value=2000,
        max_value=6000,
    )

    employment_type = factory.Faker(
        "random_element",
        elements=[
            EmployerContract.EmploymentType.PART_TIME,
            EmployerContract.EmploymentType.FULL_TIME,
        ],
    )
