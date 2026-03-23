import pytest
from tests.factories import UserFactory, TopicFactory

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

@pytest.mark.django_db
def test_user_only_sees_own_topics(authenticated_client, user):
    """
    A logged-in user should only see their own topics.
    """

    # Create another user
    other_user = UserFactory()

    # Create topics for both users
    TopicFactory(text="My Topic",
                 owner=user)

    TopicFactory(
        text="Other User Topic",
        owner=other_user)

    # Request topics page
    response = authenticated_client.get("/topics/")

    content = response.content.decode()

    assert "My Topic" in content
    assert "Other User Topic" not in content