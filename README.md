Library Management System

A Django REST API for managing a library. Users can register, log in (with JWT), search and borrow books, return them, and see a basic admin panel for management.

## Features:
1. User roles:
- Anonymous: Browse books (read-only).
- Registered: Search and borrow books.
- Admin: Manage books (add/remove), manage users, and see all loans.
2. JWT Authentication: Provided by djangorestframework-simplejwt.
3. Database Models:
- Book: Fields (title, author, ISBN, page_count, availability).
- Loan: Which user borrowed which book, borrowed_at, returned_at, etc.
- User: Standard Django User (or extended if needed).
4. Endpoints:
- POST /users/register to create a user
- POST /auth/login to get a JWT token
- GET /library/books to list books (with search/filter/pagination)
- POST /loans to borrow a book (requires JWT)
- PATCH /loans/{id} to return a book
5. Pagination & Filtering: DRF’s built-in pagination, search, and ordering for books.
6. Documentation: Auto-generated Swagger via drf-yasg.
7. Testing: Unit/integration tests with Django’s test framework (or Pytest if you prefer).
8. Docker: A Dockerfile for containerizing the app and a docker-compose.yml for local dev with PostgreSQL.
9. Heroku Deployment: Steps to containerize and deploy with Heroku’s Container Registry or the buildpack approach, plus environment variables for Postgres.

⸻

## Table of Contents:
1. Requirements
2. Quick start (local)
3. Docker & Docker Compose
4. Heroku deployment
5. Running tests
6. Swagger documentation
7. Security notes & bonus points
8. Project structure


⸻

## Requirements:
- Python 3.9+ (or the version specified in your Dockerfile)
- PostgreSQL 13+ (local or Docker)
- Django 3.2+
- Django REST Framework 3.12+
- djangorestframework-simplejwt 4.7+
- drf-yasg 1.20+
- Docker & docker-compose (for local container-based dev)
- Optionally Heroku CLI 

⸻

## Quick Start (local)

1. Clone the Repo

git clone https://github.com/wakizashi90/library_management.git

2. Create & activate virtual environment (.venv)

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

3. Install requirements.txt

pip install -r requirements.txt
4. Set up PostgreSQL locally
5. Apply migrations

python manage.py makemigrations
python manage.py migrate

6. Create a superuser

python manage.py createsuperuser

7. Run the server
python manage.py runserver

## Docker & Docker Compose
1. Build and run with Docker Compose:

docker-compose up --build
2. Go to http://127.0.0.1:8000 OR http://127.0.0.1:8000/swagger/ to see the swagger docs locally
3. To run migrations inside Docker

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

## Heroku deployment
1. heroku addons:create heroku-postgresql:hobby-dev --app <APP_NAME>
2. heroku run python manage.py migrate --app <APP_NAME>
heroku run python manage.py createsuperuser --app <APP_NAME>

Running tests using Docker:

docker-compose exec web python manage.py test


## Swagger Documentation

Once running locally on port 8000, open:
	•	Swagger UI: http://127.0.0.1:8000/swagger/
	•	ReDoc: http://127.0.0.1:8000/redoc/

You can try out endpoints. For secured endpoints, you must first log in with:

POST /auth/login

{
  "username": "testuser",
  "password": "testpass"
}

Then copy the "access" token and click Authorize in Swagger with:

Bearer <token_here>

## Security Notes & Bonus Points

- CSRF & XSS
- SQL Injection
- Filtering & Pagination: the BookViewSet allows searching by title/author and pagination with DRF’s PageNumberPagination

## Project Structure

```text
library_manager/
├─ library_manager/
│   ├─ __init__.py
│   ├─ settings.py
│   ├─ urls.py
│   ├─ wsgi.py
│   └─ asgi.py
├─ library/
│   ├─ models.py
│   ├─ views.py
│   ├─ serializers.py
│   ├─ urls.py
│   └─ admin.py
├─ loans/
│   ├─ models.py
│   ├─ views.py
│   ├─ serializers.py
│   ├─ urls.py
│   └─ admin.py
├─ users/
│   ├─ views.py
│   ├─ serializers.py
│   └─ urls.py
├─ tests/
│   ├─ test_books.py
│   ├─ test_loans.py
│   └─ test_users.py
├─ entrypoint.sh
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ runtime.txt or .python-version (for Heroku buildpack)
├─ Procfile (for Heroku, if using buildpacks)
└─ README.md
```

