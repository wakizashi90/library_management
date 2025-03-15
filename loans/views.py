from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from loans.serializers import LoanSerializer
from loans.models import Loan
from library.models import Book


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book_id', None)
        if not book_id:
            return Response({"detail": "book_id required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if not book.availability:
            return Response({"detail": "Book already borrowed"}, status=status.HTTP_400_BAD_REQUEST)

        loan = Loan.objects.create(user=user, book=book)
        book.availability = False
        book.save()

        serializer = self.get_serializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.returned_at is not None:
            return Response({"detail": "Loan already returned"}, status=status.HTTP_400_BAD_REQUEST)

        instance.returned_at = request.data.get('returned_at', None)
        if not instance.returned_at:
            from django.utils import timezone
            instance.returned_at = timezone.now()

        instance.book.availability = True
        instance.book.save()
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            queryset = Loan.objects.all()
        else:
            queryset = Loan.objects.filter(user=user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)