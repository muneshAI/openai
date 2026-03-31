from fastapi import FastAPI

from app.db import Base, engine
from app.routers import auth, progress, reminders, score, workouts

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
