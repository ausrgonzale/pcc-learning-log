import pytest
from tests.factories import EntryFactory, UserFactory, TopicFactory
from django.urls import reverse
from django.contrib.auth.models import User

from learning_logs.models import Topic, Entry

# Index Page Loads

@pytest.mark.django_db
def test_index_view_returns_200(client):
    url = reverse('learning_logs:index')

    response = client.get(url)

    assert response.status_code == 200

# Topics Require Login
@pytest.mark.django_db
def test_topics_requires_login(client):

    url = reverse('learning_logs:topics')

    response = client.get(url)

    assert response.status_code == 302
    assert "/users/login/" in response.url

# Logged-in User Can View Topics
@pytest.mark.django_db
def test_logged_in_user_can_view_topics(client):

    user = UserFactory()

    TopicFactory(
        owner=user,
        text="Python"
    )

    client.force_login(user)

    url = reverse('learning_logs:topics')

    response = client.get(url)

    assert response.status_code == 200
    assert b"Python" in response.content

# User Can View Their Own Topic
@pytest.mark.django_db
def test_user_can_view_own_topic(client):

    user = UserFactory()

    topic = TopicFactory(owner=user)

    client.force_login(user)

    url = reverse(
        'learning_logs:topic',
        args=[topic.pk]
    )

    response = client.get(url)

    assert response.status_code == 200

# User Cannot Access Another User's Topics

@pytest.mark.django_db
def test_user_cannot_access_other_users_topic(client):

    user1 = UserFactory()

    user2 = UserFactory()

    topic = TopicFactory(owner=user1)

    client.force_login(user2)

    url = reverse(
        'learning_logs:topic',
        args=[topic.pk]
    )

    response = client.get(url)

    assert response.status_code == 404

""" User Can Create a New Topic """
@pytest.mark.django_db
def test_user_can_create_topic(client):

    user = UserFactory()

    client.force_login(user)

    url = reverse('learning_logs:new_topic')

    response = client.post(
        url,
        {"text": "My New Topic"}
    )

    assert response.status_code == 302
    assert Topic.objects.count() == 1

""" User Can Create a New Entry """

@pytest.mark.django_db
def test_user_can_create_entry(client):

    user = UserFactory()

    topic = TopicFactory(owner=user)

    client.force_login(user)

    url = reverse(
        'learning_logs:new_entry',
        args=[topic.pk]
    )

    response = client.post(
        url,
        {"text": "My first entry"}
    )

    assert response.status_code == 302
    assert Entry.objects.count() == 1

""" User Can Edit an Entry """
@pytest.mark.django_db
def test_user_can_edit_entry(client):

    entry = EntryFactory()

    user = entry.topic.owner

    client.force_login(user)

    url = reverse(
        "learning_logs:edit_entry",
        args=[entry.pk]
    )

    response = client.post(
        url,
        {"text": "Updated text"}
    )

    entry.refresh_from_db()

    assert response.status_code == 302
    assert entry.text == "Updated text"

""" Get Request Returns Blank Topic Form """
@pytest.mark.django_db
def test_new_topic_get_returns_form(client):

    user = UserFactory()

    client.force_login(user)

    url = reverse('learning_logs:new_topic')

    response = client.get(url)

    assert response.status_code == 200
    assert b"<form" in response.content

""" Invalid Topic Submission Does Not Save """
@pytest.mark.django_db
def test_invalid_topic_submission(client):

    user = UserFactory()

    client.force_login(user)

    url = reverse('learning_logs:new_topic')

    response = client.post(
        url,
        {"text": ""}   # invalid
    )

    assert response.status_code == 200
    assert Topic.objects.count() == 0

""" Get Request Returns Blank Entry Form """
@pytest.mark.django_db
def test_new_entry_get_returns_form(client):

    user = UserFactory()

    topic = TopicFactory(owner=user)

    client.force_login(user)

    url = reverse(
        'learning_logs:new_entry',
        args=[topic.pk]
    )

    response = client.get(url)

    assert response.status_code == 200
    assert b"<form" in response.content

""" Get Request Returns Edit Form """
@pytest.mark.django_db
def test_edit_entry_get_returns_form(client):

    user = UserFactory()

    topic = TopicFactory(owner=user)

    entry = EntryFactory(topic=topic,text="Original")
    
    client.force_login(user)

    url = reverse(
        'learning_logs:edit_entry',
        args=[entry.pk]
    )

    response = client.get(url)

    assert response.status_code == 200
    assert b"Original" in response.content

""" User Cannot Edit Another User's Entry """
@pytest.mark.django_db
def test_user_cannot_edit_other_users_entry(client):

    owner = UserFactory()

    attacker = UserFactory()

    topic = TopicFactory(owner=owner)

    entry = EntryFactory(topic=topic)

    client.force_login(attacker)

    url = reverse(
        'learning_logs:edit_entry',
        args=[entry.pk]
    )

    response = client.get(url)

    assert response.status_code == 404

""" User Can Delete Their Own Entry """
@pytest.mark.django_db
def test_user_can_delete_entry(client):

    user = UserFactory()

    topic = TopicFactory(owner=user)

    entry = EntryFactory(topic=topic)

    client.force_login(user)

    url = reverse(
        "learning_logs:delete_entry",
        args=[entry.pk]
    )

    response = client.post(url)

    assert response.status_code == 302
    assert Entry.objects.count() == 0

""" User Cannot Delete Other Users Entries """

@pytest.mark.django_db
def test_user_cannot_delete_other_users_entry(client):

    owner = UserFactory()

    attacker = UserFactory()

    topic = TopicFactory(owner=owner)

    entry = EntryFactory(topic=topic)

    client.force_login(attacker)

    url = reverse(
        "learning_logs:delete_entry",
        args=[entry.pk]
    )

    response = client.post(url)

    assert response.status_code == 404
    assert Entry.objects.count() == 1