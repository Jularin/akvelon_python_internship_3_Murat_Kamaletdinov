from rest_framework import serializers

from task.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user instance to update, read and patch"""

    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name")


class CreateUserSerializer(UserSerializer):
    """Serializer inherited from UserSerializer and added new field to create user"""

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("password",)
