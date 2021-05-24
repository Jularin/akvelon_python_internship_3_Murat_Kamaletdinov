from django.contrib.auth.models import AbstractUser
from django.db import models

from task.managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    username = None

    first_name = models.CharField(verbose_name="name", max_length=150, blank=True)
    last_name = models.CharField(verbose_name="surname", max_length=150, blank=True)

    email = models.EmailField(verbose_name="email", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()  # manager for creating new users

    def __str__(self):
        return self.email
