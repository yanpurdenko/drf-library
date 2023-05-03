import os

import requests
from dotenv import load_dotenv
from requests import Response

load_dotenv()

URL = f"https://api.telegram.org/bot{os.environ.get('BOT_TOKEN')}/sendMessage"


def send_telegram_notification(message: str) -> Response:
    return requests.post(
        URL,
        data={
            "chat_id": os.environ.get("CHAT_ID"),
            "text": message,
        },
    )
