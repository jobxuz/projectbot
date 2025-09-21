import requests
from django.conf import settings


TELEGRAM_CHANNEL_ID="-1003043334097"

def send_telegram_message(message: str, chat_id: str = None):
    token = settings.BOT_TOKEN
    if not token:
        print("⚠️ Telegram sozlanmagan: TOKEN yo‘q")
        return

    target_id = chat_id or TELEGRAM_CHANNEL_ID

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": target_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        print("🔎 Telegram javobi:", response.status_code, response.text)
    except Exception as e:
        print("Telegram xatolik:", e)
