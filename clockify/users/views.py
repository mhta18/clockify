from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import viewsets, generics, mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser

from users.ExcelReports.export_excel import export_excel

from drf_excel.renderers import XLSXRenderer

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view

from io import BytesIO

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side,
)

from .models import User
from .permissions import IsAdminUser
from .serializers import UserSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="format",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Format output type. Set to 'xlsx' to download an Excel sheet instead of JSON.",
            enum=["xlsx"],
            required=False,
        )
    ],
    responses={
        (200, "application/json"): OpenApiResponse(
            response=UserSerializer(many=True),
            description="List of filtered users returned as JSON data on the web screen.",
        ),
        (
            200,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ): OpenApiResponse(
            response=OpenApiTypes.BINARY,
            description="Excel export file",
        ),
    },
)
class UserListAPIView(generics.ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [IsAdminUser]

    renderer_classes = [JSONRenderer, XLSXRenderer]

    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "first_name",
        "last_name",
        "country",
        "created_at",
    ]

    search_fields = [
        "email",
        "first_name",
        "last_name",
    ]

    filterset_fields = [
        "gender",
        "country",
        "created_at",
        "is_active",
        "is_admin",
    ]

    def list(self, request, *args, **kwargs):

        if request.query_params.get("format") == "xlsx":

            return export_excel.export_excel(self)

        return super().list(request, *args, **kwargs)

    

AVATAR_FORM_SCHEMA = {
    "multipart/form-data": {
        "type": "object",
        "properties": {
            "avatar": {
                "type": "string",
                "format": "binary",
            },
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "gender": {"type": "string", "enum": ["Male", "Female", "Other"]},
            "birth_date": {"type": "string", "format": "date"},
            "phone_number": {"type": "string"},
            "email": {"type": "string", "format": "email"},
        },
    }
}


@extend_schema_view(
    create=extend_schema(request=AVATAR_FORM_SCHEMA),  # POST /users/
    update=extend_schema(request=AVATAR_FORM_SCHEMA),  # PUT /users/{id}/
    partial_update=extend_schema(request=AVATAR_FORM_SCHEMA),  # PATCH /users/{id}/
)
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [IsAdminUser]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )
