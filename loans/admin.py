from django.contrib import admin
from loans.models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned_at')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('borrowed_at', 'returned_at')