from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Streak, Workout


def compute_fitness_score(db: Session, user_id: int, today: date | None = None) -> int:
    today = today or date.today()
    week_start = today - timedelta(days=today.weekday())
    weekly_workouts = (
        db.query(func.count(Workout.id))
        .filter(Workout.user_id == user_id, Workout.completed.is_(True), Workout.date >= week_start)
        .scalar()
        or 0
    )
    avg_intensity = (
        db.query(func.avg(Workout.intensity))
        .filter(Workout.user_id == user_id, Workout.completed.is_(True), Workout.date >= week_start)
        .scalar()
        or 1
    )
    avg_duration = (
        db.query(func.avg(Workout.duration))
        .filter(Workout.user_id == user_id, Workout.completed.is_(True), Workout.date >= week_start)
        .scalar()
        or 0
    )
    streak = db.get(Streak, user_id)
    streak_value = streak.current_streak if streak else 0

    score = int((streak_value * 2) + (weekly_workouts * 5) + (avg_intensity * 3) + (min(avg_duration, 90) / 3))
    return min(score, 100)
