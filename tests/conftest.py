import os
import uuid
import pytest
from django.contrib.auth.models import User


# =====================================================
# Environment Configuration
# =====================================================

os.environ.setdefault(
    "DJANGO_ALLOW_ASYNC_UNSAFE",
    "true"
)

BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost:8000"
)

DEFAULT_TIMEOUT = int(
    os.getenv(
        "PLAYWRIGHT_TIMEOUT",
        "5000"
    )
)

# =====================================================
# Shared Environment Fixtures
# =====================================================

TEST_USERNAME = "testuser"
TEST_PASSWORD = "SuperPass123!"

@pytest.fixture(scope="session")
def base_url():
    """
    Base URL for the running application.
    """
    return BASE_URL


# =====================================================
# Django User Fixtures (Unit + API + E2E)
# =====================================================

@pytest.fixture
def user(db):
    """
    Create a default test user.
    """

    return User.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD
    )


@pytest.fixture
def authenticated_client(client, user):
    """
    Django test client that is already logged in.
    """

    client.force_login(user)

    return client


# =====================================================
# Playwright Fixtures (E2E)
# =====================================================

@pytest.fixture
def page_with_timeout(page):
    """
    Standardize Playwright timeout behavior.
    """

    page.set_default_timeout(
        DEFAULT_TIMEOUT
    )

    return page


@pytest.fixture
def logged_in_user(
    page_with_timeout,
    base_url,
    user
):
    """
    Log in the default test user using Playwright.
    """

    page = page_with_timeout

    page.goto(
        f"{base_url}/users/login/"
    )

    page.fill(
        'input[name="username"]',
        TEST_USERNAME
    )

    page.fill(
        'input[name="password"]',
        TEST_PASSWORD
    )

    page.get_by_role(
        "button",
        name="Log in"
    ).click()

    return page


# =====================================================
# Test Data Generators
# =====================================================

@pytest.fixture
def unique_username():

    return f"user_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def unique_topic_name():

    return f"Topic {uuid.uuid4().hex[:6]}"


@pytest.fixture
def unique_entry_text():

    return f"Entry {uuid.uuid4().hex[:6]}"