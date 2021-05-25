from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from task.models import CustomUser
from task.serializers.user_serializer import UserSerializer, CreateUserSerializer
from task.services.user import validate_create_user_data


class UserViewSet(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
):
    """Api view with basic crud"""

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def partial_update(self, request, *args, **kwargs):
        """Create partial update for patch API method"""
        instance = self.get_object()

        if isinstance(request.user, AnonymousUser):
            # checking is user is anonymous
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if instance != self.request.user:
            # checking is user trying to patch another user
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(request_body=CreateUserSerializer)
    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                ["Forgot to enter something!"], status=status.HTTP_400_BAD_REQUEST
            )
        error_messages = validate_create_user_data(
            request.data
        )  # check if data is legit

        if error_messages:
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            email,
            password,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
        )
        user.save()
        return Response(self.serializer_class(user, context={"request": request}).data)

    # TODO create user
    # TODO get user
    # TODO delete user
