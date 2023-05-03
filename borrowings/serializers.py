from datetime import date

from django.db import transaction
from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing
from borrowings.service import send_telegram_notification


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
        read_only_fields = (
            "id",
            "borrow_date",
            "actual_return_date",
            "user_id",
        )

    def create(self, validated_data):
        print(validated_data)
        with transaction.atomic():
            instance = super().create(validated_data)
            instance.book_id.inventory -= 1
            instance.book_id.save()
            message = (
                f"New borrowing:\n"
                f"Borrow date: {date.today()}\n"
                f"Expected return date: "
                f"{validated_data['expected_return_date']}\n"
                f"Book: {validated_data['book_id']}\n"
                f"User id: {self.context['request'].user.id}\n"
                f"email: {self.context['request'].user}"
            )
            send_telegram_notification(message)
            return instance


class BorrowingListRetrieveSerializer(serializers.ModelSerializer):
    book_id = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
