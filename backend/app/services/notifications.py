from datetime import datetime

from firebase_admin import credentials, initialize_app, messaging

from app.config import settings

firebase_app = None


def init_firebase() -> None:
    global firebase_app
    if firebase_app or not settings.fcm_credentials_path:
        return
    cred = credentials.Certificate(settings.fcm_credentials_path)
    firebase_app = initialize_app(cred)


def send_push(token: str, title: str, body: str, data: dict[str, str] | None = None) -> str:
    if not token:
        return 'skipped:no-token'
    init_firebase()
    message = messaging.Message(
        token=token,
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
    )
    return messaging.send(message)


def build_reminder_message(now: datetime) -> tuple[str, str]:
    return (
        'Workout Reminder',
        f"It's {now.strftime('%H:%M')}. You haven't logged a workout yet—let's keep your streak alive!",
    )
