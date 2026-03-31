from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User, Workout
from app.schemas import WorkoutCreate, WorkoutOut
from app.services.streaks import recalculate_streak

router = APIRouter(prefix='/workouts', tags=['workouts'])


@router.get('', response_model=list[WorkoutOut])
def list_workouts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Workout).filter(Workout.user_id == current_user.id).order_by(Workout.date.desc()).all()


@router.post('', response_model=WorkoutOut)
def create_workout(payload: WorkoutCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    workout = Workout(user_id=current_user.id, **payload.model_dump())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    recalculate_streak(db, current_user.id, today=payload.date)
    return workout


@router.post('/{workout_id}/complete', response_model=WorkoutOut)
def complete_workout(workout_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    if not workout:
        raise HTTPException(status_code=404, detail='Workout not found')
    workout.completed = True
    if workout.date > date.today():
        raise HTTPException(status_code=400, detail='Cannot complete future workout')
    db.commit()
    db.refresh(workout)
    recalculate_streak(db, current_user.id)
    return workout
