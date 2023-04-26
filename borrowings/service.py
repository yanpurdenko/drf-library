import requests

from requests import Response
from library_service.settings import BOT_TOKEN, CHAT_ID

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram_notification(message: str) -> Response:
    return requests.post(
        URL,
        data={
            "chat_id": CHAT_ID,
            "text": message,
        },
    )
