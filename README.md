# Munesh AI

Production-grade multi-agent system scaffold with planning, memory, parallel executors, critic loop, and synthesis.

## Architecture

- **Orchestrator Agent (CEO):** routes tasks, manages retries, tracks state.
- **Planner Agent:** builds a task graph in structured JSON.
- **Memory System:** session memory + pgvector-ready vector memory and RAG service.
- **Executor Agents (parallel):** code, web, API, and file agents with tool interfaces.
- **Critic Agent:** validates outputs and triggers retry loop.
- **Synthesizer Agent:** composes final explainable response.
- **Observability:** per-trace structured logging.
- **Dashboard:** Next.js UI for real-time-like task execution visibility.

## Run with Docker

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## Run backend locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

- `GET /v1/health`
- `POST /v1/execute`

Example payload:

```json
{
  "goal": "One prompt to build an internal CRM app",
  "context": {
    "voiceInput": true,
    "streaming": true,
    "selfImprove": true
  }
}
```

## Bonus Hooks

- Voice input flag included in API payload contract.
- Streaming-oriented UI scaffolding.
- Self-improvement possible via critic retry logs + vector memory persistence.
