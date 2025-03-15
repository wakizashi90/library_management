from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'password': '12345test',
            'email': 'testuser@example.com',
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, 201, f"Expected 201, got {response.status_code} with body {response.content}")
        self.assertTrue(User.objects.filter(username='testuser').exists())