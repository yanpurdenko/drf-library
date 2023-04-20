from rest_framework import viewsets

from books.models import Genre, Book
from books.serializers import GenreSerializer, BookSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().prefetch_related("genres")
    serializer_class = BookSerializer
