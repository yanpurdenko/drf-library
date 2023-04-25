from datetime import datetime, date, timedelta

from borrowings.models import Borrowing
from library_service.celery import app
from borrowings.service import send_telegram_notification


@app.task
def check_overdue_borrowings() -> None:
    overdue_borrowings = Borrowing.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date__lte=date.today() - timedelta(days=1),
    ).select_related("user_id")
    message = f'Список просроченных займов на {datetime.now().strftime("%Y-%m-%d")}:\n'

    if len(overdue_borrowings) == 0:
        message = "No borrowings overdue today!"
        send_telegram_notification(message)
        return

    for borrowing in overdue_borrowings:
        message += f"- {borrowing}\n"

    send_telegram_notification(message)
