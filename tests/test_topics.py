import pytest


@pytest.mark.django_db
def test_topics_page_requires_login(client):
    """Anonymous user should be redirected to login."""

    response = client.get("/topics/")

    assert response.status_code == 302


@pytest.mark.django_db
def test_logged_in_user_can_view_topics(authenticated_client):
    """Logged-in user should access topics page."""

    response = authenticated_client.get("/topics/")

    assert response.status_code == 200