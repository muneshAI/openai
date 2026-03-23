# Munesh AI

Munesh AI is a startup-grade autonomous operator designed for founders, operators, and telecom leaders in Nepal. It combines a natural-language command center, multi-agent planning/execution, durable memory, decision intelligence, and workflow automation into one production-oriented platform.

## Product thesis

Munesh AI should:
- Think like a CEO
- Act like an operator
- Execute like an automation engine

The system is optimized for:
- Telecom campaigns and market expansion workflows in Nepal
- Business automation and executive productivity
- Internal tool generation and cross-team coordination

## Core capabilities

1. **Command Center**: Converts plain-English intent into structured plans, timelines, tools, and execution graphs.
2. **Autonomous Agent System**: Research, Decision, Execution, and Coding agents collaborate through a shared orchestration layer.
3. **Automation Engine**: Connects to Gmail, Outlook, Google Drive, Slack, WhatsApp Business, calendars, CRMs, and webhook endpoints.
4. **AI App Builder**: Generates internal tools, dashboards, microsites, telecom campaign workflows, and Chrome extensions.
5. **Memory System**: Uses session memory plus long-term vector memory for preferences, business context, and prior decisions.
6. **Decision Intelligence**: Produces trade-offs, ROI, operational risk, and recommended actions.
7. **Unified UX**: Chat-first interface with live agent activity, task board, analytics, and automation history.

## Production architecture

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                             Munesh AI Platform                              │
├────────────────────────────── Frontend Layer ────────────────────────────────┤
│ Next.js App Router                                                          │
│  • Chat Command Center  • Task Board  • Agent Activity Feed                 │
│  • Automation History   • Telecom KPI Dashboard • Voice Controls            │
└───────────────┬───────────────────────────────┬──────────────────────────────┘
                │                               │
                ▼                               ▼
┌────────────────────────────┐      ┌─────────────────────────────────────────┐
│ API Gateway / BFF          │      │ Realtime Event Bus                      │
│ FastAPI                    │      │ WebSockets / SSE / Queue notifications  │
│  • Auth / RBAC             │      │  • Agent state updates                  │
│  • Command ingestion       │      │  • Task progress                        │
│  • Rate limiting           │      │  • Analytics streams                    │
└───────────────┬────────────┘      └──────────────────┬──────────────────────┘
                │                                       │
                ▼                                       ▼
┌──────────────────────────────── Orchestration Core ──────────────────────────┐
│ Planner / Router                                                             │
│  • Intent extraction                                                         │
│  • Goal decomposition                                                        │
│  • Tool selection                                                            │
│  • Policy guardrails                                                         │
│                                                                              │
│ Multi-Agent Runtime                                                          │
│  • Research Agent                                                            │
│  • Decision Agent                                                            │
│  • Execution Agent                                                           │
│  • Coding Agent                                                              │
│  • Supervisor / Human approval gate                                          │
└───────────────┬──────────────────────────────┬────────────────────────────────┘
                │                              │
                ▼                              ▼
┌────────────────────────────┐      ┌─────────────────────────────────────────┐
│ Memory & Knowledge         │      │ Automation / Integration Layer          │
│  • PostgreSQL              │      │  • Gmail / Outlook                      │
│  • Redis cache             │      │  • Slack / WhatsApp Business API        │
│  • Vector DB               │      │  • Google Drive / Dropbox               │
│  • Audit log storage       │      │  • Calendar / CRM / ERP / Webhooks      │
└───────────────┬────────────┘      └──────────────────┬──────────────────────┘
                │                                       │
                ▼                                       ▼
┌────────────────────────────┐      ┌─────────────────────────────────────────┐
│ Intelligence Services      │      │ Delivery / Infrastructure               │
│  • LLM provider abstraction│      │  • Vercel (web)                         │
│  • ROI & risk scoring      │      │  • AWS ECS / EKS / Lambda (API/jobs)    │
│  • Recommendation engine   │      │  • Pinecone / Weaviate                  │
│  • Prompt registry         │      │  • CloudWatch / OpenTelemetry           │
└────────────────────────────┘      └─────────────────────────────────────────┘
```

## Folder structure

```text
munesh-ai/
├── README.md
├── infra/
│   └── docker-compose.yml
├── apps/
│   ├── api/
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── main.py
│   │       ├── core/
│   │       │   └── config.py
│   │       ├── models/
│   │       │   └── schemas.py
│   │       ├── routes/
│   │       │   ├── analytics.py
│   │       │   └── commands.py
│   │       └── services/
│   │           ├── decision_engine.py
│   │           ├── memory.py
│   │           └── orchestrator.py
│   └── web/
│       ├── package.json
│       ├── postcss.config.js
│       ├── tailwind.config.ts
│       ├── tsconfig.json
│       ├── app/
│       │   ├── globals.css
│       │   ├── layout.tsx
│       │   └── page.tsx
│       ├── components/
│       │   ├── ActivityLog.tsx
│       │   ├── ChatShell.tsx
│       │   └── TaskBoard.tsx
│       └── lib/
│           └── types.ts
```

## Design principles

### 1. CEO-grade command center
- Every command becomes a typed goal object with deliverables, owners, execution path, risk level, and target metrics.
- Telecom-oriented prompts include market, geography, channel mix, compliance assumptions, and campaign economics.

### 2. Agentic execution with control points
- The supervisor agent decomposes work and routes subtasks to specialist agents.
- High-risk actions such as sending mass outreach, approving budget, or touching production systems require human approval.
- All agent decisions are logged for auditing and postmortems.

### 3. Nepal and telecom optimization
- Template workflows for prepaid recharge growth, distributor enablement, field operations, tower maintenance scheduling, and campaign launches.
- Cost models can be localized to NPR and segmented by province, carrier channel, and enterprise customer tier.
- WhatsApp and SMS channels are first-class citizens for market execution in Nepal.

### 4. Startup-grade reliability
- API rate limiting, idempotency keys, integration retries, observability, and role-based access are included from day one.
- The AI layer is provider-agnostic so OpenAI, Claude, or local models can be switched without rewriting orchestration logic.

## Key backend flows

### Natural-language command lifecycle
1. User submits a command in the dashboard or voice interface.
2. API validates auth, stores the request, and sends it to the orchestrator.
3. The orchestrator extracts intent and creates a goal graph.
4. Research and Decision agents enrich the goal with context, constraints, and options.
5. Execution and Coding agents either perform integrations or generate artifacts/code.
6. Results, memory writes, analytics events, and suggested next actions are returned to the UI.

### Example telecom use case
**Input:** “Launch a telecom campaign in Nepal”

**Munesh AI output should include:**
- Province-level target segments
- Channel mix across WhatsApp, email, SMS, and partner field teams
- Timeline with approvals and dependencies
- Estimated budget in NPR
- ROI hypothesis and risk flags
- Draft outreach assets and dashboard tracking plan

## Deployment guide

### Frontend on Vercel
1. Import `apps/web` as a Vercel project.
2. Configure environment variables for API base URL, auth provider, analytics keys, and voice provider.
3. Enable edge caching for read-heavy analytics endpoints.
4. Use preview deployments for prompt, UX, and workflow validation.

### Backend on AWS
1. Containerize `apps/api` with FastAPI and deploy to ECS Fargate for predictable scaling.
2. Use PostgreSQL on Amazon RDS and Redis on ElastiCache.
3. Run asynchronous jobs via SQS + worker service for scraping, automation, and report generation.
4. Store audit logs and generated artifacts in S3.
5. Expose API through API Gateway or an ALB with WAF and rate limiting.
6. Use Secrets Manager for OAuth credentials and model provider keys.

### Vector and analytics services
- Use Pinecone or Weaviate for long-term memory and knowledge retrieval.
- Use OpenTelemetry + CloudWatch + Grafana for tracing, alerts, and system health.
- Stream task execution events into a warehouse for agent-performance analytics.

## Security model

- OAuth 2.0 for third-party integrations
- JWT session tokens for clients
- Role-based access for admins, operators, and analysts
- Encrypted secrets, scoped API tokens, and provider-specific least privilege
- Human-in-the-loop approval gates for sensitive automations
- Complete audit trail for prompt, tool, and execution events

## Future roadmap

### Phase 1: Foundation
- Command center
- Agent orchestration
- Core integrations
- Basic memory and approvals

### Phase 2: Nepal telecom operator suite
- Campaign copilot for subscriber acquisition
- Distributor and field force workflows
- SLA-driven network operations assistant
- Province-level analytics and budgeting

### Phase 3: Autonomous operating system
- Self-optimizing workflows
- Cross-tenant learning with privacy controls
- Mobile operator app for voice-first approvals
- Marketplace for industry playbooks and integrations

### Phase 4: Scale to millions of users
- Multi-region inference routing
- Tenant isolation with sharded data planes
- Event-driven microservices and queue-based agent execution
- Cost-aware model routing and adaptive caching
- Dedicated observability, security, and reliability squads

## Bonus capabilities

### Voice command support
- Browser microphone capture on web
- Speech-to-text for command intake
- Text-to-speech for summaries, approvals, and daily briefings

### Mobile app
- React Native client for approvals, chat, and live campaign alerts
- Offline-safe summaries for field teams and leadership

### Real-time analytics dashboard
- Live task states, throughput, automation savings, campaign ROI, and agent utilization
- Drill-down views for telecom campaign performance and operational bottlenecks
