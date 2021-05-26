import factory
from factory.django import DjangoModelFactory

import random

from task.tests.factories.user_factory import UserFactory
from task.models import Transaction


class TransactionFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    amount = round(random.random() * random.randint(100, 10000), 2)

    class Meta:
        model = Transaction


