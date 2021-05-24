from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from task.models import CustomUser
from task.serializers.user_serializer import UserSerializer


class UserViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
