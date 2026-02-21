# Skill: Error Handling & Debugging
**Domain:** debugging
**Version:** 1.0
**Eval Score:** —

## Description
Systematically diagnose, triage, and resolve errors. Covers reading stack traces, isolating root causes, adding structured error handling, and writing regression tests. Prioritizes upstream fixes over downstream workarounds.

## Usage
1. **Read the error** — Identify the exception type, message, and stack trace origin.
2. **Reproduce** — Write a minimal test that triggers the exact error.
3. **Isolate** — Binary-search through the call chain to find the root cause.
4. **Fix at source** — Patch the root cause, not a symptom.
5. **Add guardrails** — Add validation, error handling, or type checks to prevent recurrence.
6. **Regression test** — Ensure the failing test now passes and stays in the suite.

## Error Handling Patterns

### Structured exception hierarchy
```python
# exceptions.py — project-wide error types
class AppError(Exception):
    """Base for all application errors."""
    def __init__(self, message: str, code: str, status: int = 500):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(self.message)

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} {resource_id} not found",
            code="NOT_FOUND",
            status=404,
        )

class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"Validation failed on '{field}': {reason}",
            code="VALIDATION_ERROR",
            status=422,
        )

class ExternalServiceError(AppError):
    def __init__(self, service: str, detail: str):
        super().__init__(
            message=f"{service} error: {detail}",
            code="EXTERNAL_SERVICE_ERROR",
            status=502,
        )
```

### Catching and re-raising with context
```python
import logging

logger = logging.getLogger(__name__)

def get_user(user_id: str) -> User:
    try:
        row = db.query("SELECT * FROM users WHERE id = %s", [user_id])
    except DatabaseError as e:
        logger.error("DB query failed for user %s: %s", user_id, e)
        raise ExternalServiceError("database", str(e)) from e
    if not row:
        raise NotFoundError("User", user_id)
    return User(**row)
```

### Global error handler (Flask example)
```python
@app.errorhandler(AppError)
def handle_app_error(error: AppError):
    return {"error": error.code, "message": error.message}, error.status

@app.errorhandler(Exception)
def handle_unexpected(error: Exception):
    logger.exception("Unhandled error: %s", error)
    return {"error": "INTERNAL", "message": "An unexpected error occurred"}, 500
```

## Debugging Checklist
- [ ] **Read the full stack trace** — bottom frame is the crash site, but root cause is often higher.
- [ ] **Check recent changes** — `git log --oneline -5` and `git diff HEAD~1` to find what changed.
- [ ] **Reproduce with a test** — write a failing test *before* fixing.
- [ ] **Isolate variables** — comment out code, add print/log statements, use a debugger.
- [ ] **Check inputs** — log the actual values at the crash site. Are they what you expect?
- [ ] **Check types** — especially in Python: `None` where you expected a string, `str` where you expected `int`.
- [ ] **Search for similar issues** — check `learning/reflection-log.md` and `SOPs/` for prior art.
- [ ] **Fix at root** — don't add a `try/except` to silence an error that shouldn't happen.
- [ ] **Add regression test** — the test that exposed the bug must stay in the suite.

## Logging Best Practices
```python
# Use structured fields, not string interpolation
logger.info("User created", extra={"user_id": user.id, "email": user.email})

# Log at appropriate levels
logger.debug("Cache hit for key %s", key)         # Noisy, dev only
logger.info("Order processed: %s", order_id)       # Normal operations
logger.warning("Rate limit approaching: %d/100", count)  # Attention needed
logger.error("Payment failed for order %s", order_id)    # Action required
logger.critical("Database connection pool exhausted")     # Immediate action
```

## Eval Method
- **Metric:** Root-cause accuracy — does the fix address the actual root cause (not a symptom)?
- **Test:** Inject 5 known bugs → measure how many are correctly diagnosed and fixed at source.
- **Threshold:** ≥ 80% root-cause fixes (not workarounds).
