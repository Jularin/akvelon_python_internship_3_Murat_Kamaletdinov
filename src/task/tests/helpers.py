from rest_framework import serializers


def get_writable_serializer_fields(
    serializer: serializers.ModelSerializer,
) -> list:  # get not read only serializer fields
    writable_fields = [
        key for key, field in serializer().get_fields().items() if not field.read_only
    ]
    return writable_fields
