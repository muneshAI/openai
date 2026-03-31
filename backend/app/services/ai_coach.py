from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Workout


def recommendation_for_user(db: Session, user_id: int, today: date | None = None) -> str:
    today = today or date.today()
    last_14 = today - timedelta(days=14)
    completed = (
        db.query(func.count(Workout.id))
        .filter(Workout.user_id == user_id, Workout.completed.is_(True), Workout.date >= last_14)
        .scalar()
        or 0
    )
    if completed < 4:
        return 'Start with a 20-minute moderate workout today to rebuild consistency.'
    if completed < 8:
        return 'Great momentum. Add one high-intensity session this week for a score boost.'
    return 'You are consistent—schedule an active recovery day to avoid burnout.'
