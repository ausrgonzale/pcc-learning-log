import factory
from factory.django import DjangoModelFactory
from typing import cast
from django.contrib.auth.models import User
from learning_logs.models import Topic, Entry


class UserFactory(DjangoModelFactory):
    class Meta:  # type: ignore[override]
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(  # type: ignore[attr-defined]
        lambda n: f"user{n}"
    )

    @factory.post_generation #type: ignore[attr-defined]
    def password(self, create, extracted, **kwargs):
        user = cast(User, self)

        password = extracted or "password123"
        user.set_password(password)

        if create:
            user.save()

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