#!/bin/sh

CONFIG_FILE="config/test_config.yaml"

echo "Reading test configuration..."

RESET_DB=$(grep reset_database_before_tests $CONFIG_FILE | awk '{print $2}')
FIXTURE=$(grep fixture_file $CONFIG_FILE | awk '{print $2}')

if [ "$RESET_DB" = "true" ]; then

    echo "Resetting database..."

    rm -f db.sqlite3

    python manage.py migrate

    python manage.py loaddata $FIXTURE

else

    echo "Skipping database reset."

fi

echo "Running tests..."

pytest