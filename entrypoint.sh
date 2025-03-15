#!/bin/bash
set -e

echo "Waiting for PostgreSQL to become available at $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is up - running migrations..."

python manage.py migrate

if [ "$ENV" = "development" ]; then
  python manage.py loaddata default_books.json
fi

if [ "$ENV" = "production" ]; then
  exec gunicorn library_manager.wsgi:application --bind 0.0.0.0:8000
else
  exec python manage.py runserver 0.0.0.0:8000
fi