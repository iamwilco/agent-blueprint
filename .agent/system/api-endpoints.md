# API Endpoints
> Populate during `initialize.md`. Update when routes are added or changed.

## Conventions
| Property | Standard |
|---|---|
| Base URL | `/api/v1` |
| Auth | Bearer JWT in `Authorization` header |
| Versioning | URL path prefix (`/v1`, `/v2`) |
| Error format | `{ "error": { "code": "string", "message": "string", "details": {} } }` |
| Pagination | `?page=1&per_page=20` → response includes `total`, `page`, `per_page` |
| Date format | ISO 8601 (`2025-01-15T09:30:00Z`) |

## Endpoint Catalog
| Method | Path | Purpose | Auth | Request Body | Response |
|---|---|---|---|---|---|
| GET | `/health` | Health check | No | — | `200 { "status": "ok" }` |
| POST | `/api/v1/auth/login` | Authenticate | No | `{ "email", "password" }` | `200 { "token": "jwt..." }` |
| POST | `/api/v1/auth/register` | Create account | No | `{ "email", "name", "password" }` | `201 { "user": {...} }` |
| GET | `/api/v1/projects` | List projects | Yes | — | `200 { "data": [...], "total": N }` |
| POST | `/api/v1/projects` | Create project | Yes | `{ "name", "description" }` | `201 { "project": {...} }` |
| GET | `/api/v1/projects/:id/tasks` | List tasks | Yes | — | `200 { "data": [...] }` |
| POST | `/api/v1/projects/:id/tasks` | Create task | Yes | `{ "title", "assignee_id" }` | `201 { "task": {...} }` |
| PATCH | `/api/v1/tasks/:id` | Update task | Yes | `{ "status", "title" }` | `200 { "task": {...} }` |
| DELETE | `/api/v1/tasks/:id` | Delete task | Yes | — | `204` |

## Example Contract
```json
// POST /api/v1/auth/login
// Request
{ "email": "user@example.com", "password": "s3cret" }

// Response 200
{ "token": "eyJhbGciOi...", "expires_in": 3600 }

// Response 401
{ "error": { "code": "INVALID_CREDENTIALS", "message": "Email or password is incorrect." } }
```
