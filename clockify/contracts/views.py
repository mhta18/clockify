from django.shortcuts import render
from .serializers import EmployerContractSerializer, FreelanserContractSerializer
from .models import FreelancerContract, EmployerContract
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, mixins, viewsets
from users.permissions import IsAdminUser

FREELANCER_CONTRACT_SCHEMA = {
    "multipart/form-data": {
        "type": "object",
        "required": [
            "user",
            "role_title",
            "start_date",
            "end_date",
            "hourly_payment",
            "daily_hours_required",
        ],
        "properties": {
            "user": {
                "type": "integer",
                "description": "The unique ID of the user account associated with this contract.",
            },
            "role_title": {
                "type": "string",
                "maxLength": 255,
                "description": "The official internal job title designating the worker's responsibilities.",
            },
            "start_date": {
                "type": "string",
                "format": "date",
                "description": "The exact calendar start date of the contract engagement (YYYY-MM-DD format).",
            },
            "end_date": {
                "type": "string",
                "format": "date",
                "description": "The scheduled final termination/end date of the contract engagement (YYYY-MM-DD format).",
            },
            "hourly_payment": {
                "type": "string",
                "format": "decimal",
                "description": "The fixed billing compensation amount distributed per tracked hour (e.g., '50.00').",
            },
            "daily_hours_required": {
                "type": "integer",
                "minimum": 0,
                "description": "The daily target hour allocation expected to be clocked by the freelancer.",
            },
            "document_file": {
                "type": "string",
                "format": "uri",
                "nullable": False,
                "description": "A secure URL link or binary path to the signed physical agreement paper profile.",
            },
        },
    }
}


EMPLOYER_CONTRACT_SCHEMA = {
    "multipart/form-data": {
        "type": "object",
        "required": ["user", "role_title", "start_date", "end_date", "monthly_payment"],
        "properties": {
            "user": {
                "type": "integer",
                "description": "The unique ID of the user account associated with this contract.",
            },
            "role_title": {
                "type": "string",
                "maxLength": 255,
                "description": "The official internal job title designating the employee's responsibilities.",
            },
            "start_date": {
                "type": "string",
                "format": "date",
                "description": "The exact calendar start date of full-time or part-time employment (YYYY-MM-DD format).",
            },
            "end_date": {
                "type": "string",
                "format": "date",
                "description": "The contract expiration or evaluation review check date (YYYY-MM-DD format).",
            },
            "monthly_payment": {
                "type": "string",
                "format": "decimal",
                "description": "The gross salary compensation payout calculated per full working month calendar cycle (e.g., '3520.00').",
            },
            "employment_type": {
                "type": "integer",
                "enum": [4, 5, 6, 7, 8],
                "default": 8,
                "description": "Designated daily contractual obligation commitment hours. 4-7 denote Part-time shifts; 8 denotes standard Full-time operations.",
            },
        },
    }
}


class FreelancerContractListAPiView(generics.ListAPIView):
    queryset = FreelancerContract.objects.all()
    serializer_class = FreelanserContractSerializer
    permission_classes = [IsAdminUser]


class EmployerContractListAPIView(generics.ListAPIView):
    queryset = EmployerContract.objects.all()
    serializer_class = EmployerContractSerializer
    permission_classes = [IsAdminUser]


FREELANCER_CONTRACT_SCHEMA_VIEW = extend_schema_view(
    create=extend_schema(
        summary="Create a new freelancer contract",
        description=(
            "Allows administrators or HR personnel to generate a new hourly-rated contract. "
            "Requires direct payment definitions and specific daily targeted allocation metrics."
        ),
        request=FREELANCER_CONTRACT_SCHEMA,
    ),
    update=extend_schema(
        summary="Replace an existing freelancer contract",
        description="Completely replaces an active freelancer agreement row item. Restricted to administrative users.",
        request=FREELANCER_CONTRACT_SCHEMA,
    ),
    partial_update=extend_schema(
        summary="Patch an existing freelancer contract",
        description="Partially updates values (e.g., updating the end_date or attaching a missing document file).",
        request=FREELANCER_CONTRACT_SCHEMA,
    ),
)


class FreelancerContractViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = FreelancerContract.objects.all()
    serializer_class = FreelanserContractSerializer
    permission_classes = [IsAdminUser]


EMPLOYER_CONTRACT_SCHEMA_VIEW = extend_schema_view(
    create=extend_schema(
        summary="Create a new employer contract",
        description=(
            "Generates a standard salary contract matching specified monthly payment tiers. "
            "Automatically assigns an implied hourly calculation engine based on selected part-time or full-time types."
        ),
        request=EMPLOYER_CONTRACT_SCHEMA,
    ),
    update=extend_schema(
        summary="Replace an existing employer contract",
        description="Completely updates a running salary contract payload record. Restricted to administrative users.",
        request=EMPLOYER_CONTRACT_SCHEMA,
    ),
    partial_update=extend_schema(
        summary="Patch an existing employer contract",
        description="Partially modifies fields on a salary contract. Restricted to administrative users.",
        request=EMPLOYER_CONTRACT_SCHEMA,
    ),
)


class EmployerContractViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = EmployerContract.objects.all()
    serializer_class = EmployerContractSerializer
    permission_classes = [IsAdminUser]
