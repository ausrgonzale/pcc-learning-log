import pytest
from django.contrib.auth.models import User
from learning_logs.models import Topic, Entry


@pytest.mark.django_db
def test_entry_str_representation():
    """Entry string should start with entry text."""

    user = User.objects.create_user(
        username="testuser",
        password="password123"
    )

    topic = Topic.objects.create(
        text="Python",
        owner=user
    )

    entry = Entry.objects.create(
        topic=topic,
        text="My first entry"
    )

    assert str(entry).startswith("My first entry")