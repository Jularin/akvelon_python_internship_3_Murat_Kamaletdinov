import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient():
    """function generate APIClient instance"""
    return APIClient()
