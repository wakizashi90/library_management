#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate

if [ "$ENV" = "development" ]; then
  python manage.py makemigrations

  python << END
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_manager.settings')
import django
django.setup()
from django.contrib.auth.models import User
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("Superuser already exists or not configured.")
END

  python manage.py loaddata default_books.json
fi

if [ "$ENV" = "production" ]; then
  exec gunicorn library_manager.wsgi:application --bind 0.0.0.0:8000
else
  exec python manage.py runserver 0.0.0.0:8000
fi