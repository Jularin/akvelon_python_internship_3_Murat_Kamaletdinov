from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin, ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from task.models import CustomUser
from task.serializers.user_serializer import UserSerializer, CreateUserSerializer
from task.services.user import validate_create_user_data


class UserViewSet(
    GenericViewSet,
    DestroyModelMixin
):
    """Api view with basic CRUD"""

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def partial_update(self, request: Request, *args, **kwargs):
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
    def create(self, request: Request, *args, **kwargs):
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

    @swagger_auto_schema(operation_id="user_read", request_body=no_body, responses={200: UserSerializer()})
    @action(methods=["GET"], url_path="", detail=False, permission_classes=(IsAuthenticated,))
    def get_current_user(self, request: Request):
        return Response(self.serializer_class(self.request.user, context={"request": request}).data)

    def destroy(self, request: Request, *args, **kwargs):
        try:
            if CustomUser.objects.get(pk=request.parser_context["kwargs"]["pk"]) != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request.user.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

