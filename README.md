# AI-Powered Fitness Tracker (Expo + FastAPI)

Production-ready monorepo with a React Native (Expo) mobile app and FastAPI backend using PostgreSQL, Redis, Celery, JWT auth, and FCM reminders.

## Architecture

- **Mobile:** React Native + Expo + Zustand + Victory charts
- **API:** FastAPI + SQLAlchemy + JWT
- **DB:** PostgreSQL
- **Scheduling:** Celery worker + Celery beat + Redis
- **Notifications:** Firebase Cloud Messaging (server push)
- **AI Coach:** Rule-based fallback with OpenAI-ready integration point

## Backend API

Swagger is available at:
- `http://localhost:8000/docs`

REST endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `GET|POST /workouts`
- `POST /workouts/{id}/complete`
- `GET /progress`
- `GET /score`
- `GET /score/dashboard`
- `GET|PUT /reminders/settings`

## Database Schema

### users
- `id` (PK)
- `email` (unique)
- `password_hash`
- `timezone`
- `reminder_time`
- `reminders_enabled`
- `fcm_token`

### workouts
- `id` (PK)
- `user_id` (FK users.id)
- `date`
- `type`
- `duration`
- `intensity`
- `calories`
- `notes`
- `completed`
- `created_at`

### streaks
- `user_id` (PK/FK users.id)
- `current_streak`
- `longest_streak`
- `updated_at`

## Reminder Logic

Celery Beat runs every 15 minutes and checks each user's local timezone window:

```python
if reminders_enabled and local_time matches reminder_time window:
    if no completed workout exists for local date:
        send FCM notification
```

This avoids duplicate sends by only triggering in a single time window and only when no completed workout exists for the day.

## Fitness Score Engine

`score = (streak * 2) + (weekly_workouts * 5) + intensity_factor + duration_factor`

Score is capped at 100.

## Local Setup

1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Start backend stack:
   ```bash
   docker compose up --build
   ```
3. Backend available at `http://localhost:8000`.
4. Run mobile app:
   ```bash
   cd frontend
   npm install
   npm run start
   ```

## Testing

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

## Deployment

- Backend deploys as Docker containers (API, Celery worker, Celery beat).
- PostgreSQL and Redis run as managed services or containers.
- CI executes backend tests via GitHub Actions.
- Mobile app can be built with EAS (`eas build --platform ios|android`).
