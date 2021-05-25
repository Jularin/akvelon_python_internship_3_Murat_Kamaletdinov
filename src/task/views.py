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
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from task.models import CustomUser
from task.serializers.user_serializer import UserSerializer


class UserViewSet(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
):
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
