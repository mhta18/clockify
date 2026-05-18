from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets,generics,mixins
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.renderers import JSONRenderer
from drf_excel.renderers import XLSXRenderer
from django_filters.rest_framework import DjangoFilterBackend
from drf_excel.mixins import XLSXFileMixin

from .models import User
from .permissions import IsAdminUser
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser,FormParser


@extend_schema(
    responses={
        (
            200,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ): OpenApiResponse(
            response=OpenApiTypes.BINARY,
            description="Excel export file",
        ),
    }
)
class UserListAPIView(XLSXFileMixin, generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    # sorting by created_at field
    ordering_fields = ['first_name', 'last_name', 'country']
    # searching by email and first_name fields
    search_fields = ['email', 'first_name']
    # filtering by gender, country and created_at fields
    filterset_fields = ['gender', 'country', 'created_at']

    renderer_classes = [JSONRenderer,XLSXRenderer]
    filename = "users.xlsx"


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
        FormParser
    )
    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'avatar': {
                        'type': 'string',
                        'format': 'binary'
                    },
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'gender': {'type': 'string', 'enum': ['Male', 'Female', 'Other']},
                    'birth_date': {'type': 'string', 'format': 'date'},
                    'phone_number': {'type': 'string'},
                    'email': {'type': 'string', 'format': 'email'},
                }
            }
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
