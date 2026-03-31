from datetime import date, datetime, time

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default='UTC')
    reminder_time: Mapped[time] = mapped_column(Time, default=time(6, 0))
    reminders_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    fcm_token: Mapped[str | None] = mapped_column(String(512), nullable=True)

    workouts: Mapped[list['Workout']] = relationship(back_populates='user', cascade='all,delete-orphan')
    streak: Mapped['Streak'] = relationship(back_populates='user', uselist=False, cascade='all,delete-orphan')


class Workout(Base):
    __tablename__ = 'workouts'
    __table_args__ = (UniqueConstraint('user_id', 'date', 'type', name='uq_user_workout_type_date'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    intensity: Mapped[int] = mapped_column(Integer, default=1)
    calories: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped['User'] = relationship(back_populates='workouts')


class Streak(Base):
    __tablename__ = 'streaks'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped['User'] = relationship(back_populates='streak')
