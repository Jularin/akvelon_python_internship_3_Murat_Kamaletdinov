import factory
from factory.django import DjangoModelFactory

from task.models import CustomUser


class UserFactory(DjangoModelFactory):
    """Factory to create user instances for tests"""

    email = factory.LazyAttribute(
        lambda a: f"{a.first_name.lower()}.{a.last_name.lower()}@example.com"
    )
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = CustomUser
