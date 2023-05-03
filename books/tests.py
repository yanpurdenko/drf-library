from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Book, Genre
from books.serializers import BookSerializer, GenreSerializer
from users.tests import create_user

BOOK_URL = reverse("books:book-list")
GENRE_URL = reverse("books:genre-list")


def sample_books(**params):
    defaults = {
        "title": "Test",
        "author": "Test",
        "inventory": 10,
        "daily_fee": 1.00,
        "cover": "Hard",
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_genres(**params):
    defaults = {
        "name": "Test",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


class PublicBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_book_list(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_list(self):
        response = self.client.get(GENRE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_post(self):
        payload = {
            "title": "Test",
            "author": "Test",
            "inventory": 10,
            "daily_fee": 1.00,
            "cover": "Hard",
        }
        response = self.client.post(BOOK_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_retrieve(self):
        sample_books()
        response = self.client.get(f"{BOOK_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_post(self):
        payload = {
            "name": "Test",
        }
        response = self.client.post(GENRE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_book_list(self):
        sample_books()
        response = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_genre_list(self):
        sample_genres()
        response = self.client.get(GENRE_URL)
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_post(self):
        payload = {
            "title": "Test",
            "author": "Test",
            "inventory": 10,
            "daily_fee": 1.00,
            "cover": "Hard",
        }
        response = self.client.post(BOOK_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_retrieve(self):
        sample_books()
        response = self.client.get(f"{BOOK_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_post(self):
        payload = {
            "name": "Test",
        }
        response = self.client.post(GENRE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_book_post(self):
        payload = {
            "title": "Test",
            "author": "Test",
            "inventory": 10,
            "daily_fee": 1.00,
            "cover": "Hard",
        }
        response = self.client.post(BOOK_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_retrieve(self):
        sample_books()
        response = self.client.get(f"{BOOK_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_put(self):
        sample_books()
        payload = {
            "title": "Test Title",
            "author": "Test Author",
            "inventory": 100,
            "daily_fee": 1.00,
            "cover": "Hard",
        }
        response = self.client.put(f"{BOOK_URL}1/", payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_patch(self):
        sample_books()
        payload = {
            "inventory": 500,
            "daily_fee": 4.00,
        }
        response = self.client.patch(f"{BOOK_URL}1/", payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_delete(self):
        sample_books()
        response = self.client.delete(f"{BOOK_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_genre_post(self):
        payload = {
            "name": "Test",
        }
        response = self.client.post(GENRE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genre_retrieve(self):
        sample_genres()
        response = self.client.get(f"{GENRE_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_put(self):
        sample_genres()
        payload = {
            "name": "Test",
        }

        response = self.client.put(f"{GENRE_URL}1/", payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_patch(self):
        sample_genres()
        payload = {
            "name": "Test Name",
        }
        response = self.client.patch(f"{GENRE_URL}1/", payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_delete(self):
        sample_genres()
        response = self.client.delete(f"{GENRE_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
