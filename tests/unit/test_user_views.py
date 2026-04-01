import pytest
from tests.unit.factories import UserFactory
from django.urls import reverse
from django.contrib.auth.models import User

""" Registration Page Loads """
@pytest.mark.django_db
def test_register_page_returns_200(client):

    url = reverse("users:register")

    response = client.get(url)

    assert response.status_code == 200

""" User Can Register Successfully """
@pytest.mark.django_db
def test_user_can_register(client):

    url = reverse("users:register")

    response = client.post(
        url,
        {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()

""" Invalid Registration Fails """
@pytest.mark.django_db
def test_invalid_registration(client):

    url = reverse("users:register")

    response = client.post(
        url,
        {
            "username": "",
            "password1": "pass",
            "password2": "different",
        },
    )

    assert response.status_code == 200
    assert User.objects.count() == 0

""" Test Logout Redirect Works """
@pytest.mark.django_db
def test_logout_redirects(client):

    user = UserFactory()

    client.login(
        username=user.username,
        password="testpass123"
    )

    response = client.post(
        reverse("users:logout")
    )

    assert response.status_code == 302