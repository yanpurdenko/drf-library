from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import Q

from borrowings.models import Borrowing
from borrowings.service import send_telegram_notification
from library_service.celery import app


@app.task
def check_overdue_borrowings() -> None:
    overdue_borrowings = Borrowing.objects.filter(
        Q(expected_return_date__lt=date.today()) & Q(actual_return_date=None)
    )

    if overdue_borrowings.exists():
        for borrowing in overdue_borrowings:
            user = get_user_model().objects.get(id=borrowing.user_id.id)
            message = (
                f"Overdue borrowing:\n"
                f"id: {borrowing.id}\n"
                f"Borrow date: {borrowing.borrow_date}\n"
                f"Expected return date: "
                f"{borrowing.expected_return_date}\n"
                f"Overdue days: {date.today() - borrowing.expected_return_date}\n"
                f"Book: {borrowing.book_id}\n"
                f"User id: {borrowing.user_id}\n"
                f"Email: {user.email}"
            )
            send_telegram_notification(message)
    else:
        send_telegram_notification(message="No borrowings overdue today!")
