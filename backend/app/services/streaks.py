from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models import Streak, Workout


def recalculate_streak(db: Session, user_id: int, today: date | None = None) -> Streak:
    today = today or date.today()
    streak = db.get(Streak, user_id)
    if not streak:
        streak = Streak(user_id=user_id, current_streak=0, longest_streak=0)
        db.add(streak)
        db.flush()

    current = 0
    cursor = today
    while True:
        completed = (
            db.query(Workout)
            .filter(Workout.user_id == user_id, Workout.date == cursor, Workout.completed.is_(True))
            .first()
        )
        if not completed:
            break
        current += 1
        cursor -= timedelta(days=1)

    streak.current_streak = current
    streak.longest_streak = max(streak.longest_streak, current)
    db.commit()
    db.refresh(streak)
    return streak
