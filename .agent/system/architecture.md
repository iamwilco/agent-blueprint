# System Architecture
> Populate during `initialize.md` or `update.md`. Keep current as the system evolves.

## High-Level Overview
<!-- One-paragraph summary of what the system does and who it serves. -->
Example: A web service that exposes a REST API for [domain]. The backend processes requests, persists state in a relational database, and dispatches async jobs via a message queue. A single-page app consumes the API.

## Components
| Component | Technology | Responsibility | Repo Path |
|---|---|---|---|
| API Server | Python / Flask | REST endpoints, auth, validation | `src/api/` |
| Worker | Python / Celery | Async jobs (email, reports, sync) | `src/worker/` |
| Frontend | React / TypeScript | SPA, user-facing UI | `frontend/` |
| Database | PostgreSQL 15 | Persistent state, ACID transactions | `migrations/` |
| Cache / Queue | Redis 7 | Session store, Celery broker | — |
| Reverse Proxy | Nginx | TLS termination, rate limiting | `infra/nginx.conf` |

## Data Flows
```
User ──▶ Nginx ──▶ Flask API ──▶ PostgreSQL
                       │
                       ├──▶ Redis (cache hit?)
                       │
                       └──▶ Celery Worker ──▶ External Services
                                │
                                └──▶ PostgreSQL (write results)
```
1. **Request ingress:** User hits Nginx → proxied to Flask.
2. **Auth & validation:** JWT verified; request schema validated.
3. **Business logic:** Service layer processes; reads/writes DB.
4. **Async dispatch:** Long-running work enqueued to Celery via Redis.
5. **Response:** JSON response returned; cache populated if applicable.

## Key Design Decisions
| Decision | Rationale | Date |
|---|---|---|
| Flask over Django | Lighter footprint; explicit routing preferred | YYYY-MM-DD |
| Celery for async | Mature, Redis-backed, retries built-in | YYYY-MM-DD |
| PostgreSQL over NoSQL | Relational model fits domain; strong ACID | YYYY-MM-DD |

## Non-Functional Requirements
- **Reliability:** Health checks at `/health`; Celery retry with exponential backoff.
- **Scalability:** Stateless API servers behind load balancer; horizontal worker scaling.
- **Security:** JWT auth, CORS whitelist, rate limiting via Nginx, secrets in env vars.
- **Observability:** Structured JSON logs; Prometheus metrics at `/metrics`.
