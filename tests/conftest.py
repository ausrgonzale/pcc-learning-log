import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="password123"
    )

@pytest.fixture
def authenticated_client(client, user):
    """
    Log in the test user automatically
    and return the authenticated client.
    
    """
    client.force_login(user)
    return client