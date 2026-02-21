# SOP: Third-Party API Integration Setup
**Category:** integrations
**Created:** 2025-01-20
**Last Used:** 2025-02-10
**Trigger:** When integrating a new external API (payment, email, analytics, etc.)

## Problem
Integrating third-party APIs without a consistent pattern leads to:
- Scattered API keys across config files
- No retry/backoff logic, causing cascading failures
- Missing error handling for provider-specific error codes
- No mocking strategy, making tests brittle or slow

## Prerequisites
- API credentials (key, secret, or OAuth client) stored in environment variables
- Provider documentation URL bookmarked
- Rate limit info documented (requests/sec, daily quota)

## Procedure

### Step 1 — Create an adapter module
Create a dedicated module that wraps the third-party SDK or HTTP calls:
```
src/integrations/<provider-name>/
├── __init__.py
├── client.py       # Wrapper class with retry logic
├── models.py       # Request/response data classes
├── exceptions.py   # Provider-specific exception types
└── mock.py         # Fake client for testing
```

### Step 2 — Implement the client with retry logic
```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ProviderClient:
    def __init__(self, api_key: str, base_url: str, timeout: float = 10.0):
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def call_endpoint(self, path: str, payload: dict) -> dict:
        response = self.client.post(path, json=payload)
        response.raise_for_status()
        return response.json()
```

### Step 3 — Map provider errors to application errors
```python
from .exceptions import ProviderRateLimitError, ProviderAuthError

def handle_provider_error(status_code: int, body: dict):
    if status_code == 429:
        raise ProviderRateLimitError(retry_after=body.get("retry_after", 60))
    elif status_code == 401:
        raise ProviderAuthError("Invalid API key — check env var")
    elif status_code >= 500:
        raise ProviderUnavailableError("Provider is down — retry later")
```

### Step 4 — Create a mock for testing
```python
class MockProviderClient:
    """Drop-in replacement for ProviderClient in tests."""
    def __init__(self, responses: dict[str, dict] | None = None):
        self.responses = responses or {}
        self.calls: list[tuple[str, dict]] = []

    def call_endpoint(self, path: str, payload: dict) -> dict:
        self.calls.append((path, payload))
        return self.responses.get(path, {"status": "ok"})
```

### Step 5 — Register in dependency injection / config
```python
# config.py
INTEGRATIONS = {
    "provider_name": {
        "api_key_env": "PROVIDER_API_KEY",
        "base_url": "https://api.provider.com/v1",
        "rate_limit": "100/min",
        "timeout": 10.0,
    }
}
```

### Step 6 — Add health check
Add the provider to your health check endpoint so monitoring catches outages:
```python
async def check_provider_health():
    try:
        client.call_endpoint("/health", {})
        return {"provider_name": "healthy"}
    except Exception as e:
        return {"provider_name": f"unhealthy: {e}"}
```

### Step 7 — Document in system/architecture.md
Add the integration to the architecture doc:
- Component name and purpose
- Data flow (what goes in, what comes out)
- Failure mode (what happens when provider is down)

## Verification
- [ ] API key is in env var, not hardcoded
- [ ] Client has retry with exponential backoff
- [ ] Provider errors are mapped to application exceptions
- [ ] Mock client exists and is used in all tests
- [ ] Health check includes the provider
- [ ] Rate limits are documented in config
- [ ] Integration is documented in `system/architecture.md`

## Related
- `system/architecture.md` — update component diagram
- `skills/testing/integration-testing/SKILL.md` — use for writing integration tests
- `guidelines/agent-behavior.md` — follow error handling rules
