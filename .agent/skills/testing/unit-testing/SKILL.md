# Skill: Unit Testing
**Domain:** testing
**Version:** 1.1
**Eval Score:** 0.70

## Description
Design robust, isolated unit tests following Arrange-Act-Assert (AAA). Prioritize edge cases, error paths, and boundary conditions. Tests should be deterministic, fast, and independent.

## Usage
1. Identify the function/method under test and its contract (inputs → outputs + side effects).
2. List test cases: happy path, edge cases, error paths, boundary values.
3. Write each test using AAA pattern.
4. Mock external dependencies (DB, network, file I/O) — never hit real services.
5. Assert both return values and side effects (e.g., mock call counts).
6. Name tests descriptively: `test_<behavior>_when_<condition>_should_<expected>`.

## Code Snippet
```python
import pytest
from unittest.mock import patch, MagicMock

def test_create_user_returns_user_object(db_session):
    """Happy path: valid input returns a User."""
    user = create_user(db_session, email="test@example.com", name="Test")
    assert user.email == "test@example.com"
    assert user.id is not None

def test_create_user_raises_on_duplicate_email(db_session):
    """Error path: duplicate email raises ValueError."""
    create_user(db_session, email="dup@example.com", name="First")
    with pytest.raises(ValueError, match="already exists"):
        create_user(db_session, email="dup@example.com", name="Second")

def test_create_user_strips_whitespace(db_session):
    """Edge case: leading/trailing whitespace is stripped."""
    user = create_user(db_session, email="  spaced@example.com  ", name=" Name ")
    assert user.email == "spaced@example.com"
    assert user.name == "Name"

@patch("myapp.services.email.send")
def test_create_user_sends_welcome_email(mock_send, db_session):
    """Side effect: welcome email is dispatched."""
    create_user(db_session, email="new@example.com", name="New")
    mock_send.assert_called_once_with(to="new@example.com", template="welcome")
```

## Test Case Generation Checklist
| Category | Example |
|---|---|
| Happy path | Valid input → expected output |
| Empty/null input | `None`, `""`, `[]`, `{}` |
| Boundary values | `0`, `-1`, `MAX_INT`, empty string |
| Duplicate/conflict | Unique constraint violation |
| Permission denied | Unauthorized access attempt |
| External failure | Network timeout, DB connection error (mocked) |

## Eval Method
- **Metric:** Mutation testing survival rate via `mutmut` or equivalent.
- **Command:** `mutmut run --paths-to-mutate=src/ --tests-dir=tests/`
- **Threshold:** ≥70% mutants killed = pass.
