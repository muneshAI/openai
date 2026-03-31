from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import ReminderSettingsUpdate, UserOut

router = APIRouter(prefix='/reminders', tags=['reminders'])


@router.get('/settings', response_model=UserOut)
def get_settings(current_user: User = Depends(get_current_user)):
    return current_user


@router.put('/settings', response_model=UserOut)
def update_settings(
    payload: ReminderSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.reminders_enabled = payload.reminders_enabled
    current_user.reminder_time = payload.reminder_time
    current_user.timezone = payload.timezone
    db.commit()
    db.refresh(current_user)
    return current_user
