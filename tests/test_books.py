from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_superuser(
            username='admin', email='admin@test.com', password='adminpass'
        )

    def test_create_book_admin(self):
        login_res = self.client.post('/api/auth/login/', {
            'username': 'admin',
            'password': 'adminpass'
        }, format='json')
        self.assertEqual(login_res.status_code, 200, f"Login failed: {login_res.content}")
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            "title": "Admin Created Book",
            "author": "Author Admin",
            "isbn": "99998",
            "page_count": 200,
            "availability": True
        }
        response = self.client.post('/api/library/books/', data, format='json')
        self.assertEqual(response.status_code, 201, f"Expected 201, got {response.status_code} with body {response.content}")
        self.assertEqual(response.data['title'], 'Admin Created Book')