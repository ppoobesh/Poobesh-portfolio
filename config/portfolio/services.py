import os
import requests
from django.conf import settings

def send_telegram_notification(contact_message):

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        return False

    telegram_url = (
        f"https://api.telegram.org/"
        f"bot{bot_token}/sendMessage"
    )

    text = (
        "📩 New Portfolio Contact Message\n\n"
        f"Name: {contact_message.sender_name}\n"
        f"Email: {contact_message.sender_email}\n"
        f"Subject: {contact_message.subject or 'No subject'}\n\n"
        f"Message:\n{contact_message.message}"
    )

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    try:
        response = requests.post(
            telegram_url,
            data=payload,
            timeout=10,
        )

        return response.ok

    except requests.RequestException:
        return False