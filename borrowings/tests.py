import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListRetrieveSerializer
from users.tests import create_user

BORROWING_URL = reverse("borrowings:borrowing-list")


def borrowing_detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


class PublicBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email="test@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            is_staff=False,
        )
        self.book = Book.objects.create(
            title="Test",
            author="Test",
            inventory=10,
            daily_fee=1.00,
            cover="Hard",
        )

    def test_borrowing_list_unauthorized(self):
        response = self.client.get(BORROWING_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_borrowing_post_unauthorized(self):
        payload = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today() + datetime.timedelta(days=2),
            "book_id": self.book.id,
            "user_id": self.user,
        }
        response = self.client.post(BORROWING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email="test@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            is_staff=False,
        )
        self.book = Book.objects.create(
            title="Test",
            author="Test",
            inventory=10,
            daily_fee=1.00,
            cover="Hard",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def sample_borrowing(self, **params):
        defaults = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today() + datetime.timedelta(days=2),
            "book_id": self.book,
            "user_id": self.user,
        }
        defaults.update(params)
        return Borrowing.objects.create(**defaults)

    def test_filter_borrowings_by_active(self):
        self.sample_borrowing()
        self.sample_borrowing()
        active_borrowings = Borrowing.objects.filter(actual_return_date__isnull=True)
        response = self.client.get(f"{BORROWING_URL}?is_active=1")
        response_borrowings = 0
        for _ in list(response.data.values())[3]:
            response_borrowings += 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_borrowings, active_borrowings.count())

    def test_borrowing_return(self):
        borrowing = self.sample_borrowing()
        url = f"{borrowing_detail_url(borrowing.id)}return/"
        response = self.client.post(url)
        borrowing.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrowing_post(self):
        payload = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today() + datetime.timedelta(days=3),
            "book_id": self.book.id,
            "user_id": self.user,
        }
        response = self.client.post(BORROWING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_borrowing_list(self):
        self.sample_borrowing()
        borrowings = Borrowing.objects.all()
        serializer = BorrowingListRetrieveSerializer(borrowings, many=True)
        response = self.client.get(BORROWING_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.values())[3], serializer.data)

    def test_borrowing_retrieve(self):
        borrowing = self.sample_borrowing()
        response = self.client.get(borrowing_detail_url(borrowing.id))
        serializer = BorrowingListRetrieveSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_borrowing_put_not_allowed(self):
        payload = {
            "borrow_date": datetime.date.today(),
            "expected_return_date": datetime.date.today() + datetime.timedelta(days=8),
            "book_id": self.book.id,
            "user_id": self.user,
        }
        borrowing = self.sample_borrowing()
        response = self.client.put(borrowing_detail_url(borrowing.id), payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_borrowing_patch_not_allowed(self):
        payload = {
            "expected_return_date": datetime.datetime.today() + datetime.timedelta(days=8)
        }
        borrowing = self.sample_borrowing()
        response = self.client.patch(borrowing_detail_url(borrowing.id), payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_borrowing_delete_not_allowed(self):
        borrowing = self.sample_borrowing()
        response = self.client.delete(borrowing_detail_url(borrowing.id))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
