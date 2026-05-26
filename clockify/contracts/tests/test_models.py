import pytest
from django.test import TestCase
from users.tests.factories import UserFactory
from .factories import FreelancerFactory, EmployerFactory
from django.db import IntegrityError

@pytest.mark.django_db
class ContractModelTest(TestCase):

    def setUp(self):
        self.user_admin = UserFactory.create(is_admin=True)
        self.user = UserFactory.create()

    def test_user_can_not_have_multiple_contract_with_different_roles(self):

        FreelancerFactory(
            user=self.user, role_title="Backend Developer"
        )
        with self.assertRaises(IntegrityError):
            EmployerFactory(
                user=self.user,
                role_title="Different Employer Position", 
            )
