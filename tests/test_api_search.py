import pytest
from django.urls import reverse
from tests.factories import TopicFactory, EntryFactory

@pytest.mark.django_db
def test_user_can_search_topics(authenticated_client, user):
    """
    User can search their topics by text.
    """

    TopicFactory(text="Python", owner=user)
    TopicFactory(text="Django", owner=user)

    url = reverse("api:topics")

    response = authenticated_client.get(
        url,
        {"search": "Python"},
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 1
    assert results[0]["text"] == "Python"


@pytest.mark.django_db
def test_search_returns_empty_when_no_match(authenticated_client, user):
    """
    Search returns empty list when no topics match.
    """

    TopicFactory(text="Python", owner=user)

    url = reverse("api:topics")

    response = authenticated_client.get(
        url,
        {"search": "Java"},
    )

    assert response.status_code == 200

    results = response.json()

    assert results == []


@pytest.mark.django_db
def test_search_requires_authentication(client, user):
    """
    Unauthenticated users cannot search topics.
    """

    TopicFactory(text="Python", owner=user)

    url = reverse("api:topics")

    response = client.get(
        url,
        {"search": "Python"},
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_user_can_filter_entries_by_topic(authenticated_client, user):
    """
    User can filter entries by topic.
    """

    topic1 = TopicFactory(owner=user)
    topic2 = TopicFactory(owner=user)

    # Create entries and keep reference to one we expect back
    entry1 = EntryFactory(topic=topic1)
    EntryFactory(topic=topic2)

    url = reverse("api:entries")

    response = authenticated_client.get(
        url,
        {"topic": topic1.pk},
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 1

    result = results[0]
    
    assert result["id"] == entry1.pk
    assert result["topic"] == topic1.pk

     # Optional: confirm field exists without matching exact value
    assert "date_added" in result

@pytest.mark.django_db
def test_filter_returns_empty_when_topic_has_no_entries(
    authenticated_client,
    user,
):
    """
    Filtering by a topic with no entries returns an empty list.
    """

    topic_with_entries = TopicFactory(owner=user)
    topic_without_entries = TopicFactory(owner=user)

    EntryFactory(topic=topic_with_entries)

    url = reverse("api:entries")

    response = authenticated_client.get(
        url,
        {"topic": topic_without_entries.pk},
    )

    assert response.status_code == 200

    results = response.json()

    assert results == []

@pytest.mark.django_db
def test_entry_filter_requires_authentication(client, user):
    """
    Unauthenticated users cannot filter entries by topic.
    """

    topic = TopicFactory(owner=user)
    EntryFactory(topic=topic)

    url = reverse("api:entries")

    response = client.get(
        url,
        {"topic": topic.pk},
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_user_can_order_topics_by_date(authenticated_client, user):
    """
    User can order topics by date_added.
    """

    topic1 = TopicFactory(owner=user)
    topic2 = TopicFactory(owner=user)

    url = reverse("api:topics")

    response = authenticated_client.get(
        url,
        {"ordering": "date_added"},
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 2

    # Oldest first when ordering ascending
    assert results[0]["id"] == topic1.pk
    assert results[1]["id"] == topic2.pk

@pytest.mark.django_db
def test_user_can_order_topics_descending_by_date(
    authenticated_client,
    user,
):
    topic1 = TopicFactory(owner=user)
    topic2 = TopicFactory(owner=user)

    url = reverse("api:topics")

    response = authenticated_client.get(
        url,
        {"ordering": "-date_added"},
    )

    assert response.status_code == 200

    results = response.json()

    assert results[0]["id"] == topic2.pk
    assert results[1]["id"] == topic1.pk
