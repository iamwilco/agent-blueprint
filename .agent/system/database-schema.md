# Database Schema
> Populate during `initialize.md`. Update when migrations are added.

## Store Configuration
| Property | Value |
|---|---|
| Engine | PostgreSQL 15 |
| Migration tool | Alembic (Python) / Prisma (Node) / Flyway (JVM) |
| Naming convention | `snake_case` tables and columns |
| Soft deletes | `deleted_at` timestamp where applicable |

## Entity-Relationship Diagram
```
┌───────────┐       ┌───────────────┐       ┌───────────┐
│   users   │──1:N──│   projects    │──1:N──│   tasks   │
│           │       │               │       │           │
│ id (PK)   │       │ id (PK)       │       │ id (PK)   │
│ email     │       │ owner_id (FK) │       │ project_id│
│ name      │       │ name          │       │ title     │
│ created_at│       │ created_at    │       │ status    │
└───────────┘       └───────────────┘       │ assignee  │
                                            │ created_at│
                                            └───────────┘
```

## Tables
| Table | Purpose | Key Columns | Relationships |
|---|---|---|---|
| `users` | User accounts | `id`, `email`, `name`, `password_hash`, `created_at` | Has many `projects` |
| `projects` | Workspace grouping | `id`, `owner_id`, `name`, `description`, `created_at` | Belongs to `users`; has many `tasks` |
| `tasks` | Work items | `id`, `project_id`, `title`, `status`, `assignee_id`, `created_at` | Belongs to `projects` and `users` |
| `audit_log` | Change tracking | `id`, `entity_type`, `entity_id`, `action`, `payload`, `created_at` | Polymorphic reference |

## Indexes
- `users(email)` — unique, for login lookups.
- `projects(owner_id)` — for user's project listing.
- `tasks(project_id, status)` — composite, for filtered task queries.
- `audit_log(entity_type, entity_id)` — for entity history lookups.

## Constraints
- `users.email` — `UNIQUE NOT NULL`.
- `tasks.status` — `CHECK (status IN ('todo','in_progress','done','blocked'))`.
- All `_id` foreign keys — `ON DELETE CASCADE` or `SET NULL` as appropriate.
- `created_at` — defaults to `NOW()`.
