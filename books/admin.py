from django.contrib import admin

from books.models import Genre, Book


admin.site.register(Genre)
admin.site.register(Book)
