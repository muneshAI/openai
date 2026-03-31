# AI-Powered Fitness Tracker (Expo + FastAPI)

Production-ready monorepo with a React Native (Expo) mobile app and FastAPI backend using PostgreSQL, Redis, Celery, JWT auth, and FCM reminders.

## Architecture

- **Mobile:** React Native + Expo + Zustand + Victory charts
- **API:** FastAPI + SQLAlchemy + JWT
- **DB:** PostgreSQL
- **Scheduling:** Celery worker + Celery beat + Redis (container mode) or Vercel Cron fallback
- **Notifications:** Firebase Cloud Messaging (server push)
- **AI Coach:** Rule-based fallback with OpenAI-ready integration point

## Backend API

Swagger is available at:
- `http://localhost:8000/docs` (local)
- `https://<your-vercel-domain>/docs` (Vercel)

REST endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `GET|POST /workouts`
- `POST /workouts/{id}/complete`
- `GET /progress`
- `GET /score`
- `GET /score/dashboard`
- `GET|PUT /reminders/settings`
- `GET /cron/reminders` (cron-triggered reminder dispatch)

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

- **Container mode**: Celery Beat runs every 15 minutes and dispatches reminders.
- **Vercel mode**: Vercel Cron hits `/cron/reminders` every 15 minutes.

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

## Deploy to Vercel (Backend API)

1. Install Vercel CLI and login:
   ```bash
   npm i -g vercel
   vercel login
   ```
2. Deploy from repo root:
   ```bash
   vercel --prod
   ```
3. Configure these Vercel environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL` (managed Postgres URL)
   - `FCM_CREDENTIALS_PATH` (optional if you load creds another way)
   - `AUTO_CREATE_TABLES=false` (recommended with migrations)
   - `CRON_SECRET=<strong-random-value>`
4. Confirm Vercel Cron is active from `vercel.json` (`*/15 * * * *` for `/cron/reminders`).
5. Set the mobile app API base URL to your Vercel URL in `EXPO_PUBLIC_API_URL`.

> Note: Expo mobile binaries are built with EAS; Vercel hosts the backend API, not native app binaries.

## Testing

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

## Deployment

- Backend deploys as Docker containers (API, Celery worker, Celery beat) or as a Vercel Python function.
- PostgreSQL and Redis run as managed services or containers.
- CI executes backend tests via GitHub Actions.
- Mobile app can be built with EAS (`eas build --platform ios|android`).
