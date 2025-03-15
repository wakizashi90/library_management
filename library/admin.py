from django.contrib import admin
from library.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'availability')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('availability',)