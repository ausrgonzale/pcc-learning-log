import factory
from factory.django import DjangoModelFactory

from django.contrib.auth.models import User
from learning_logs.models import Topic, Entry


class UserFactory(DjangoModelFactory):
    class Meta:  # type: ignore[override]
        model = User

    username = factory.Sequence(  # type: ignore[attr-defined]
        lambda n: f"user{n}"
    )

    password = factory.PostGenerationMethodCall(  # type: ignore[attr-defined]
        "set_password",
        "testpass123"
    )


class TopicFactory(DjangoModelFactory):
    class Meta:  # type: ignore[override]
        model = Topic

    text = "Test Topic"

    owner = factory.SubFactory(  # type: ignore[attr-defined]
        UserFactory
    )


class EntryFactory(DjangoModelFactory):
    class Meta:  # type: ignore[override]
        model = Entry

    text = "Test Entry"

    topic = factory.SubFactory(  # type: ignore[attr-defined]
        TopicFactory
    )