import pytest

@pytest.mark.django_db
def test_topics_page_requires_login(client):

    response = client.get("/topics/")

    assert response.status_code == 302