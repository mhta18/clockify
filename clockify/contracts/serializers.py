from rest_framework import serializers
from .models import EmployerContract,FreelancerContract

class BaseContract(serializers.ModelSerializer):
    class Meta:
        model = EmployerContract
        fields = [
            "role_title",
            "start_date",
            "end_date",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class EmployerContractSerializer(BaseContract):
    class Meta:
        model = EmployerContract
        fields = [
            "role_title",
            "start_date",
            "end_date",
            "created_at",
            "monthly_payment",
            "employment_type"
        ]

class FreelanserContractSerializer(BaseContract):
    class Meta:
        model = FreelancerContract
        fields = [
            "role_title",
            "start_date",
            "end_date",
            "created_at",
            "hourly_payment",
            "daily_hours_required",
            "document_file",
        ]
