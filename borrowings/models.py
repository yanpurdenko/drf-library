from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q, F

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.PROTECT)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(expected_return_date__gt=F("borrow_date")),
                name="check_expected_return_date",
            ),
            models.CheckConstraint(
                check=Q(
                    Q(actual_return_date__isnull=True)
                    | Q(actual_return_date__gte=F("borrow_date")),
                ),
                name="check_actual_return_date",
            ),
        ]
        ordering = ["borrow_date"]

    @property
    def total_price(self) -> Decimal:
        return (
                self.book_id.daily_fee * (self.expected_return_date - self.borrow_date).days
        )

    @property
    def fine_price(self) -> Decimal | None:
        if self.actual_return_date is None:
            return None
        return (
                self.book_id.daily_fee
                * (self.actual_return_date - self.expected_return_date).days
        )

    def __str__(self) -> str:
        return (
            f"{self.book_id}: from {self.borrow_date} to {self.expected_return_date}."
        )
