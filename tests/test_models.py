import pytest
from tests.factories import UserFactory, TopicFactory
from learning_logs.models import Topic, Entry

@pytest.mark.django_db
def test_entry_str_representation():
    """Entry string should start with entry text."""

    user = UserFactory()

    topic = TopicFactory(
        text="Python",
        owner=user
    )

    entry = Entry.objects.create(
        topic=topic,
        text="My first entry"
    )

    assert str(entry).startswith("My first entry")