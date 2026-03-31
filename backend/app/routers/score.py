from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User, Workout
from app.schemas import DashboardOut, ScoreOut
from app.services.score import compute_fitness_score

router = APIRouter(prefix='/score', tags=['score'])


@router.get('', response_model=ScoreOut)
def get_score(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    score = compute_fitness_score(db, current_user.id)
    return ScoreOut(score=score, formula='(streak * 2) + (weekly_workouts * 5) + intensity + duration factors')


@router.get('/dashboard', response_model=DashboardOut)
def dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    workout_done_today = (
        db.query(Workout)
        .filter(Workout.user_id == current_user.id, Workout.date == today, Workout.completed.is_(True))
        .first()
        is not None
    )
    week_start = today - timedelta(days=today.weekday())
    weekly_completed = (
        db.query(func.count(Workout.id))
        .filter(Workout.user_id == current_user.id, Workout.completed.is_(True), Workout.date >= week_start)
        .scalar()
        or 0
    )
    streak = current_user.streak
    return DashboardOut(
        workout_done_today=workout_done_today,
        fitness_score=compute_fitness_score(db, current_user.id),
        current_streak=streak.current_streak if streak else 0,
        longest_streak=streak.longest_streak if streak else 0,
        weekly_completed=weekly_completed,
    )
