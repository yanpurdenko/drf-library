from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Genre, Book
from books.permissions import IsAdminUserOrReadOnly
from books.serializers import GenreSerializer, BookSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)


class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().prefetch_related("genres")
    serializer_class = BookSerializer
    pagination_class = BookPagination
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)
