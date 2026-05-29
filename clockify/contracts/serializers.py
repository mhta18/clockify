from rest_framework import serializers
from .models import Contract, EmployerContract, FreelancerContract
from users.models import User
from rest_framework.validators import UniqueValidator


class BaseContract(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        validators=[
            UniqueValidator(
                queryset=Contract.objects.all(),
                message="A contract already exists for this user.",
            )
        ],
    )

    class Meta:
        model = Contract
        fields = [
            "user",
            "role_title",
            "start_date",
            "end_date",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class EmployerContractSerializer(BaseContract):
    employment_type_display = serializers.CharField(
        source="get_employment_type_display", read_only=True
    )
    class Meta:
        model = EmployerContract 
        fields = BaseContract.Meta.fields + [
            "role_title",
            "start_date",
            "end_date",
            "created_at",
            "monthly_payment",
            "employment_type",
            "employment_type_display",
        ]


class FreelanserContractSerializer(BaseContract):
    class Meta:
        model = FreelancerContract
        fields = BaseContract.Meta.fields + [
            "role_title",
            "start_date",
            "end_date",
            "created_at",
            "hourly_payment",
            "daily_hours_required",
            "document_file",
        ]
