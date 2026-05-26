import pytest
from users.tests.factories import UserFactory
from datetime import date, timedelta
from contracts.serializers import (
    FreelanserContractSerializer,
    EmployerContractSerializer,
)
from .factories import FreelancerContractFactory, EmployerContractFactory
from contracts.models import EmployerContract

pytestmark = pytest.mark.django_db


class TestFreelancerSerializer:
    def test_valid_Freelancer_serializer(self):
        user = UserFactory()
        data = {
            "user": user.id,
            "role_title": "React Developer",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=90)),
            "hourly_payment": "45",
            "daily_hours_required": 8,
        }

        serialazer = FreelanserContractSerializer(data=data)

        assert serialazer.is_valid(), serialazer.errors
        assert serialazer.validated_data["role_title"] == "React Developer"
        assert serialazer.validated_data["user"] == user

    def test_duplicate_user_contract_fails_validation_Freelancer(self):
        existing_contract = FreelancerContractFactory()
        existing_user = existing_contract.user

        duplicate_data = {
            "user": existing_user.id,
            "role_title": "React Developer",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=90)),
            "hourly_payment": "45",
            "daily_hours_required": 8,
        }

        serializer = FreelanserContractSerializer(data=duplicate_data)

        assert not serializer.is_valid()
        assert "user" in serializer.errors


class TestFreelancerSerializer:
    def test_valid_Employer_serializer(self):
        user = UserFactory()
        data = {
            "user": user.id,
            "role_title": "React Developer",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=90)),
            "monthly_payment": "450",
            "employment_type": EmployerContract.EmploymentType.PART_TIME,
        }

        serialazer = EmployerContractSerializer(data=data)

        assert serialazer.is_valid(), serialazer.errors
        assert serialazer.validated_data["role_title"] == "React Developer"
        assert serialazer.validated_data["user"] == user

    def test_duplicate_user_contract_fails_validation_Employer(self):
        existing_contract = EmployerContractFactory()
        existing_user = existing_contract.user

        duplicate_data = {
            "user": existing_user.id,
            "role_title": "React Developer",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=90)),
            "monthly_payment": "450",
            "employment_type": EmployerContract.EmploymentType.FULL_TIME,
        }

        serializer = EmployerContractSerializer(data=duplicate_data)

        assert not serializer.is_valid()
        assert "user" in serializer.errors
