from celery import Celery

from app.config import settings

celery = Celery('fitness_tracker', broker=settings.redis_url, backend=settings.redis_url)
celery.conf.timezone = 'UTC'
celery.conf.beat_schedule = {
    'check-reminders-every-15-min': {
        'task': 'app.tasks.dispatch_due_reminders',
        'schedule': 900.0,
    }
}
