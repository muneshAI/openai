from datetime import date, time

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    timezone: str = 'UTC'


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    timezone: str
    reminder_time: time
    reminders_enabled: bool

    class Config:
        from_attributes = True


class WorkoutCreate(BaseModel):
    date: date
    type: str
    duration: int = Field(ge=0)
    intensity: int = Field(default=1, ge=1, le=5)
    calories: int = Field(default=0, ge=0)
    notes: str | None = None
    completed: bool = True


class WorkoutOut(WorkoutCreate):
    id: int

    class Config:
        from_attributes = True


class ReminderSettingsUpdate(BaseModel):
    reminders_enabled: bool
    reminder_time: time
    timezone: str


class DashboardOut(BaseModel):
    workout_done_today: bool
    fitness_score: int
    current_streak: int
    longest_streak: int
    weekly_completed: int


class ScoreOut(BaseModel):
    score: int
    formula: str


class WeeklyProgressPoint(BaseModel):
    day: str
    completed: int


class ProgressOut(BaseModel):
    weekly: list[WeeklyProgressPoint]
    monthly_completed: int
    missed_this_month: int
