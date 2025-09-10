import requests


TELEGRAM_BOT_TOKEN="8178359032:AAFXFnSOpXOsXRBq8ODmRGCGoEC2A7f6260"
TELEGRAM_CHANNEL_ID="-1003043334097"


def send_telegram_message(message: str):
    token = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_CHANNEL_ID
    if not token or not chat_id:
        print("⚠️ Telegram sozlanmagan: TOKEN yoki CHANNEL_ID yo‘q")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print("Telegram xatolik:", e)
