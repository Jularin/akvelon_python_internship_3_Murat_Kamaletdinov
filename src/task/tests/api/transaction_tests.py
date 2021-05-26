import pytest
from rest_framework import status

from task.tests.factories.transaction_factory import TransactionFactory


@pytest.mark.django_db
def test_create_transaction_success(api_client):
    pass


@pytest.mark.django_db
def test_create_transaction_fail(api_client):
    pass


@pytest.mark.django_db
def test_patch_transaction_success(api_client):
    pass


@pytest.mark.django_db
def test_patch_transaction_fail(api_client):
    pass


@pytest.mark.django_db
def test_get_transaction_success(api_client):
    pass


@pytest.mark.django_db
def test_get_transaction_fail(api_client):
    pass


@pytest.mark.django_db
def test_delete_transaction_success(api_client):
    pass


@pytest.mark.django_db
def test_delete_transaction_fail(api_client):
    pass
