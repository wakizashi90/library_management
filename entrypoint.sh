#!/bin/bash
set -e

echo "Waiting for PostgreSQL to become available at $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is up - running migrations..."

python manage.py makemigrations

python manage.py migrate

python << END
import os

# Set DJANGO_SETTINGS_MODULE manually so django.setup() knows which settings to load:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_manager.settings')

import django
django.setup()
from django.contrib.auth.models import User

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print(f"Superuser {username} already exists. Skipping.")
END

python manage.py loaddata default_books.json

exec python manage.py runserver 0.0.0.0:8000