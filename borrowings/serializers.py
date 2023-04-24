from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import serializers

from borrowings.models import Borrowing


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
            "user",
        )

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            instance.book_id.inventory -= 1
            instance.book_id.save()

            return instance