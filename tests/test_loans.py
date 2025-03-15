from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from library.models import Book
from loans.models import Loan


class LoanTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='regularuser', password='regpass'
        )
        self.book = Book.objects.create(
            title='Loanable Book',
            author='Jane Roe',
            isbn='54321',
            page_count=150,
            availability=True
        )

    def test_create_loan_anonymous(self):
        data = {'book_id': self.book.id}
        response = self.client.post('/api/loans/', data, format='json')
        self.assertEqual(response.status_code, 401, f"Expected 401, got {response.status_code} with body {response.content}")

    def test_create_loan_authenticated(self):
        login_res = self.client.post('/api/auth/login/', {
            'username': 'regularuser',
            'password': 'regpass'
        }, format='json')
        self.assertEqual(login_res.status_code, 200, f"Login failed: {login_res.content}")
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {'book_id': self.book.id}
        response = self.client.post('/api/loans/', data, format='json')
        self.assertEqual(response.status_code, 201, f"Expected 201, got {response.status_code} with body {response.content}")

        loan = Loan.objects.get(user=self.user, book=self.book)
        self.assertFalse(loan.book.availability)