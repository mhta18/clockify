import random
import factory
from django.utils import timezone
from timetracking.models import TimeLog
from users.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory
from teams.tests.factories import TeamFactory
from contracts.tests.factories import EmployerContractFactory,FreelancerContractFactory
from datetime import timedelta
from decimal import Decimal

class TimeLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeLog

    @factory.lazy_attribute
    def user(self):
        new_user = UserFactory()

        contract_factory = random.choice([EmployerContractFactory, FreelancerContractFactory])
        contract_factory(user=new_user)

        return new_user

    start_time = factory.LazyFunction(timezone.now)
    end_time = None
    description = "Coding task"
    payment = Decimal("0.00")
    @factory.lazy_attribute
    def project(self):
        team = TeamFactory(members=[self.user.id])
        return ProjectFactory(teams=[team.id])
