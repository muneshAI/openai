from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.celery_app import celery
from app.db import SessionLocal
from app.models import User, Workout
from app.services.notifications import build_reminder_message, send_push


def _should_send_now(user: User, now_utc: datetime) -> bool:
    user_local = now_utc.astimezone(ZoneInfo(user.timezone))
    return user_local.hour == user.reminder_time.hour and user_local.minute < 15


@celery.task(name='app.tasks.dispatch_due_reminders')
def dispatch_due_reminders() -> dict[str, int]:
    now_utc = datetime.now(tz=ZoneInfo('UTC'))
    sent = 0
    scanned = 0
    db: Session = SessionLocal()
    try:
        users = db.query(User).filter(User.reminders_enabled.is_(True)).all()
        for user in users:
            scanned += 1
            if not _should_send_now(user, now_utc):
                continue
            user_today = now_utc.astimezone(ZoneInfo(user.timezone)).date()
            workout_done = (
                db.query(Workout)
                .filter(Workout.user_id == user.id, Workout.date == user_today, Workout.completed.is_(True))
                .first()
            )
            if workout_done:
                continue
            title, body = build_reminder_message(now_utc)
            send_push(user.fcm_token or '', title, body, {'type': 'workout_reminder'})
            sent += 1
        return {'scanned': scanned, 'sent': sent}
    finally:
        db.close()
