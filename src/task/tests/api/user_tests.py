import pytest
from django.utils.crypto import get_random_string
from rest_framework import status

from task.models import CustomUser
from task.serializers.user_serializer import UserSerializer
from task.tests.factories.user_factory import UserFactory


# tests for user API
from task.tests.helpers import get_writable_serializer_fields


@pytest.mark.django_db
def test_get_current_user_success(api_client):
    user = UserFactory.create()
    api_client.force_authenticate(user=user)

    r = api_client.get(path="/api/user/get_current_user/")
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["email"] == user.email
    assert r.json()["first_name"] == user.first_name
    assert r.json()["last_name"] == user.last_name


def test_get_current_user_fail(api_client):
    r = api_client.get(path="/api/user/get_current_user/")

    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_user_success(api_client):
    user_data = {
        "email": get_random_string() + "@example.com",
        "first_name": get_random_string(),
        "last_name": get_random_string(),
    }

    r = api_client.post(
        path="/api/user/",
        data={**user_data, "password": get_random_string()},
        format="json",
    )

    assert r.status_code == status.HTTP_200_OK

    r_data = r.json()
    for user_create_key, user_create_value in user_data.items():
        assert r_data[user_create_key] == user_create_value


@pytest.mark.django_db
def test_crete_user_fail(api_client):
    email = get_random_string() + "@example.com"
    user_data = {
        "email": email,
        "first_name": get_random_string(),
        "last_name": get_random_string(),
        "password": email,  # send password same as email
    }

    r = api_client.post(path="/api/user/", data=user_data, format="json")

    assert r.status_code == status.HTTP_400_BAD_REQUEST

    # sending without data
    r = api_client.post(path="/api/user/")

    assert r.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patch_user_success(api_client):
    user = UserFactory.create()
    temp_user = UserFactory.create()

    temp_user_dict = temp_user.__dict__
    user_dict_to_update = dict()
    writable_serializer_fields = get_writable_serializer_fields(UserSerializer)

    for field in writable_serializer_fields:
        user_dict_to_update[field] = temp_user_dict[field]  # get fields from model

    api_client.force_authenticate(user=user)

    r = api_client.patch(
        path=f"/api/user/{user.pk}/", data=user_dict_to_update, format="json"
    )
    assert r.status_code == status.HTTP_200_OK

    r_data = r.json()

    for field in writable_serializer_fields:
        assert r_data[field] == temp_user_dict[field]


@pytest.mark.django_db
def test_patch_user_fail(api_client):
    user = UserFactory.create()
    temp_user = UserFactory.create()
    temp_user_dict = temp_user.__dict__
    user_dict_to_update = dict()

    writable_serializer_fields = get_writable_serializer_fields(UserSerializer)

    for field in writable_serializer_fields:
        user_dict_to_update[field] = temp_user_dict[field]

    r = api_client.patch(
        path=f"/api/user/{user.pk}/", data=user_dict_to_update, format="json"
    )

    assert r.status_code == status.HTTP_401_UNAUTHORIZED

    api_client.force_authenticate(user=user)
    r = api_client.patch(
        path=f"/api/user/{temp_user.pk}/", data=user_dict_to_update, format="json"
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_user_success(api_client):
    user = UserFactory.create()
    api_client.force_authenticate(user=user)

    r = api_client.delete(path=f"/api/user/{user.pk}/")

    assert r.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_user_fail(api_client):
    user = UserFactory.create()
    second_user = UserFactory.create()
    api_client.force_authenticate(user=user)

    r = api_client.delete(path=f"/api/user/{second_user.pk}/")

    assert r.status_code == status.HTTP_403_FORBIDDEN
