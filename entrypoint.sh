#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Loading initial data..."
python manage.py loaddata fixtures/initial_data.json || true

echo "Starting Django server..."
exec "$@"