import pytest
from tests.factories import UserFactory, TopicFactory

@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_authenticated, expected_status",
    [
        (False, 302),
        (True, 200),
    ],
)
def test_topics_page_access(client, user, is_authenticated, expected_status):
    """
    Topics page should require login.
    """

    if is_authenticated:
        client.force_login(user)

    response = client.get("/topics/")

    assert response.status_code == expected_status