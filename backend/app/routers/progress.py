from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User, Workout
from app.schemas import ProgressOut, WeeklyProgressPoint

router = APIRouter(prefix='/progress', tags=['progress'])


@router.get('', response_model=ProgressOut)
def get_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    weekly = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        completed = (
            db.query(func.count(Workout.id))
            .filter(Workout.user_id == current_user.id, Workout.date == day, Workout.completed.is_(True))
            .scalar()
            or 0
        )
        weekly.append(WeeklyProgressPoint(day=day.strftime('%a'), completed=int(completed > 0)))

    month_start = today.replace(day=1)
    monthly_completed = (
        db.query(func.count(Workout.id))
        .filter(Workout.user_id == current_user.id, Workout.date >= month_start, Workout.completed.is_(True))
        .scalar()
        or 0
    )
    days_elapsed = (today - month_start).days + 1
    return ProgressOut(
        weekly=weekly,
        monthly_completed=monthly_completed,
        missed_this_month=max(days_elapsed - monthly_completed, 0),
    )
