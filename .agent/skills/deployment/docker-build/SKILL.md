# Skill: Docker Build & Deploy
**Domain:** deployment
**Version:** 1.1
**Eval Score:** 0.80

## Description
Build optimized Docker images, run multi-service stacks with Compose, and deploy to container orchestrators. Follows best practices for layer caching, security, and image size.

## Usage
1. Write/update `Dockerfile` with multi-stage build.
2. Write/update `docker-compose.yml` for local dev + test.
3. Build and test locally.
4. Tag and push to registry.
5. Deploy to target (ECS, Kubernetes, Fly.io, etc.).

## Dockerfile Template (Multi-stage Python)
```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
COPY src/ src/

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /app/src src/
COPY alembic/ alembic/
COPY alembic.ini .

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
CMD ["gunicorn", "src.app:create_app()", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

## Docker Compose Template
```yaml
version: "3.9"
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/app
      REDIS_URL: redis://cache:6379/0
    depends_on:
      db: { condition: service_healthy }
      cache: { condition: service_started }

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
    volumes: ["pgdata:/var/lib/postgresql/data"]

  cache:
    image: redis:7-alpine

volumes:
  pgdata:
```

## Best Practices Checklist
- [ ] Multi-stage build (small final image).
- [ ] Non-root user in runtime stage.
- [ ] `.dockerignore` excludes `.git`, `node_modules`, `__pycache__`, `.env`.
- [ ] `HEALTHCHECK` defined.
- [ ] Secrets via env vars or mounted files, never baked into image.
- [ ] Pin base image versions (e.g., `python:3.12-slim`, not `python:latest`).
- [ ] Layer ordering: deps first (cacheable), code second (changes often).

## Eval Method
- **Metric:** Image size + build time + `docker compose up` health check pass.
- **Command:** `docker build -t app:test . && docker images app:test --format '{{.Size}}'`
- **Threshold:** Image <500MB; health check passes within 30s.
