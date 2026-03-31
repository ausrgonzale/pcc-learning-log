#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings


def ensure_database_ready():
    """
    Ensure database schema and required users exist.

    Behavior:
    - If database/tables missing → run migrations
    - If admin user missing → load fixtures
    - Otherwise → do nothing

    Runs only when starting the development server.
    """

    if "runserver" not in sys.argv:
        return

    try:
        import django
        django.setup()

        from django.db import connection
        from django.core.management import call_command
        from django.contrib.auth import get_user_model

        print("Checking database state...")

        # --------------------------------------------------
        # Step 1 — Ensure migrations applied
        # --------------------------------------------------
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='django_migrations';"
            )
            migrations_table = cursor.fetchone()

        if not migrations_table:
            print("Database not initialized. Running migrations...")
            call_command("migrate", interactive=False)

        # --------------------------------------------------
        # Step 2 — Ensure admin user exists
        # --------------------------------------------------
        User = get_user_model()

        if not User.objects.filter(username="admin").exists():
            print("Admin user not found. Loading fixtures...")
            fixture_path = settings.INITIAL_DATA_FIXTURE
            call_command(
                "loaddata",
                fixture_path
            )
            print("Fixtures loaded.")

        else:
            print("Admin user already exists.")

    except Exception as exc:
        print(f"Startup initialization failed: {exc}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "learning_log.settings"
    )

    ensure_database_ready()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed "
            "and available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()