import pytest
import json
from django.urls import reverse

from learning_logs.models import Topic
from tests.factories import UserFactory, TopicFactory


@pytest.mark.django_db
def test_api_requires_authentication(client):
    """Unauthenticated users should be blocked."""
    response = client.get("/api/topics/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_only_sees_own_topics(client):
    """Authenticated user should only see their own topics."""

    user1 = UserFactory()
    user2 = UserFactory()

    topic1 = TopicFactory(owner=user1)
    TopicFactory(owner=user2)

    client.force_login(user1)

    url = reverse("api:topics")

    response = client.get(url)

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == topic1.pk


@pytest.mark.django_db
def test_user_can_create_topic(client):
    """Authenticated user can create a topic via the API."""

    user = UserFactory()

    client.force_login(user)

    url = reverse("api:topics")

    payload = {
        "text": "New API Topic"
    }

    response = client.post(
        url,
        payload,
        format="json",
    )

    assert response.status_code == 201

    assert Topic.objects.filter(
        text="New API Topic",
        owner=user,
    ).exists()

@pytest.mark.django_db
def test_user_can_update_topic(client):
    """Authenticated user can update their own topic."""

    user = UserFactory()

    topic = TopicFactory(
        owner=user,
        text="Original Topic",
    )

    client.force_login(user)

    url = reverse(
        "api:topic-detail",
        args=[topic.pk],
    )

    payload = {
        "text": "Updated Topic",
    }

    response = client.patch(
    url,
    data=json.dumps(payload),
    content_type="application/json",
    )

    topic.refresh_from_db()

    assert response.status_code == 200
    assert topic.text == "Updated Topic"

@pytest.mark.django_db
def test_user_can_delete_topic(client):
    """Authenticated user can delete their own topic."""

    user = UserFactory()

    topic = TopicFactory(owner=user)

    client.force_login(user)

    url = reverse(
        "api:topic-detail",
        args=[topic.pk],
    )

    response = client.delete(url)

    assert response.status_code == 204

    assert not Topic.objects.filter(
        pk=topic.pk
    ).exists()