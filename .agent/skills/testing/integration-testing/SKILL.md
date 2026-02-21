# Skill: Integration Testing
**Domain:** testing
**Version:** 1.1
**Eval Score:** 0.80

## Description
Design tests that verify behavior across component boundaries: API endpoints, database interactions, message queues, and external service integrations. Uses real (or containerized) dependencies, not mocks.

## Usage
1. Identify the integration boundary under test (e.g., API→DB, Service→Queue, Service→ExternalAPI).
2. Set up test infrastructure: Docker containers for DB/Redis, test fixtures, seed data.
3. Write tests that exercise the full path through the boundary.
4. Assert on observable outcomes: DB state, HTTP responses, queue messages.
5. Clean up state between tests (transaction rollback or truncation).

## Code Snippet
```python
import pytest
import httpx
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def postgres():
    with PostgresContainer("postgres:15") as pg:
        yield pg.get_connection_url()

@pytest.fixture
def client(postgres):
    app = create_app(database_url=postgres)
    with httpx.Client(app=app, base_url="http://test") as c:
        yield c

def test_create_and_retrieve_project(client):
    """Full roundtrip: create via POST, retrieve via GET, verify DB state."""
    # Create
    resp = client.post("/api/v1/projects", json={"name": "Test Project"})
    assert resp.status_code == 201
    project_id = resp.json()["project"]["id"]

    # Retrieve
    resp = client.get(f"/api/v1/projects/{project_id}")
    assert resp.status_code == 200
    assert resp.json()["project"]["name"] == "Test Project"

def test_create_project_with_invalid_data(client):
    """Error path: missing required field returns 422."""
    resp = client.post("/api/v1/projects", json={})
    assert resp.status_code == 422
    assert "name" in resp.json()["error"]["message"].lower()

def test_delete_project_cascades_tasks(client):
    """Cascade: deleting project removes its tasks."""
    resp = client.post("/api/v1/projects", json={"name": "Temp"})
    pid = resp.json()["project"]["id"]
    client.post(f"/api/v1/projects/{pid}/tasks", json={"title": "Task 1"})

    client.delete(f"/api/v1/projects/{pid}")

    resp = client.get(f"/api/v1/projects/{pid}/tasks")
    assert resp.status_code == 404
```

## Test Infrastructure Patterns
| Pattern | Use Case | Tool |
|---|---|---|
| Testcontainers | Real DB/Redis in Docker | `testcontainers-python` |
| Factory fixtures | Seed consistent test data | `factory_boy` / `faker` |
| Transaction rollback | Fast cleanup between tests | `pytest-postgresql` |
| VCR cassettes | Record/replay HTTP to external APIs | `vcrpy` |

## Eval Method
- **Metric:** Boundary coverage — % of API endpoints with ≥1 integration test.
- **Command:** Cross-reference route list (`flask routes`) with test file greps.
- **Threshold:** ≥80% endpoint coverage = pass.
