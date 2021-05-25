from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError

from task.models import CustomUser


def validate_create_user_data(data: dict) -> list:
    """Email and password validation"""
    error_messages = []

    if CustomUser.objects.filter(email=data.get("email")).exists():
        error_messages.append("Email has already been taken")

    error_messages.extend(validate_password(data))

    return error_messages


def validate_password(sign_up_data: dict) -> list:
    """Password validation"""
    error_messages = []

    try:
        password = sign_up_data.get("password")
        password_validation.validate_password(password=password)

        # We create a temporary user, which we do not write to database,
        # in order to check the password with UserAttributeSimilarityValidator
        UserAttributeSimilarityValidator().validate(
            password, CustomUser(email=sign_up_data.get("email"))
        )

    except ValidationError as e:
        for password_error in e.error_list:
            error_messages.extend(password_error.messages)

    return error_messages
