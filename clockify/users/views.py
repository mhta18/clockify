from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets,generics,mixins
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from .models import User
from .permissions import IsAdminUser
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser,FormParser


@extend_schema(
    # This forces Swagger to stop expecting a URI string
    # and start expecting a Binary file.
    request={"multipart/form-data": UserSerializer},
)
class UserListAPIView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]

    ordering_fields = ['first_name', 'last_name', 'country','gender']
    ordering = ["created_at"]
    search_fields = ['email', 'first_name']
    filterset_fields = ['gender', 'country']

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
                        'format': 'binary' # This is the "magic" line for Swagger
                    },
                    # Add other fields here if you want them to show up in the same form
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
