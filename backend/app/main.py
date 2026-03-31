from fastapi import FastAPI, Header, HTTPException

from app.config import settings
from app.db import Base, engine
from app.routers import auth, progress, reminders, score, workouts
from app.tasks import dispatch_due_reminders

if settings.auto_create_tables:
    Base.metadata.create_all(bind=engine)

app = FastAPI(title='AI Fitness Tracker API', version='1.0.0')

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(progress.router)
app.include_router(score.router)
app.include_router(reminders.router)


@app.get('/healthz', tags=['system'])
def healthz():
    return {'status': 'ok'}


@app.get('/cron/reminders', tags=['system'])
def run_reminder_cron(authorization: str | None = Header(default=None)):
    if settings.cron_secret:
        expected = f'Bearer {settings.cron_secret}'
        if authorization != expected:
            raise HTTPException(status_code=401, detail='Unauthorized cron invocation')
    return dispatch_due_reminders()
