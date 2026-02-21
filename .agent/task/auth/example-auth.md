# Task: User Authentication System
**Domain:** auth
**Status:** done
**Created:** 2025-01-15
**Updated:** 2025-01-22

## Context
The application needs a secure authentication system supporting email/password login, OAuth2 social providers (Google, GitHub), and JWT-based session management. Currently there is no auth — all endpoints are unprotected.

## Goal
Users can register, log in (email or OAuth), receive a JWT access + refresh token pair, and access protected endpoints. Unauthorized requests return 401.

## Scope
- **In scope:**
  - Email/password registration with bcrypt hashing
  - Login endpoint returning JWT access (15 min) + refresh (7 day) tokens
  - OAuth2 flow for Google and GitHub
  - Middleware to protect routes (`@require_auth` decorator)
  - Password reset via email link
  - Rate limiting on login (5 attempts / minute)
- **Out of scope:**
  - MFA / 2FA (follow-up task)
  - Admin role management (separate task)
  - Session revocation dashboard

## Plan
1. Design DB schema: `users`, `oauth_accounts`, `refresh_tokens` tables (est. 2h)
2. Implement registration endpoint with input validation (est. 3h)
3. Implement login endpoint with JWT generation (est. 2h)
4. Implement refresh token rotation (est. 2h)
5. Add `@require_auth` middleware and apply to protected routes (est. 1h)
6. Integrate Google OAuth2 flow (est. 3h)
7. Integrate GitHub OAuth2 flow (est. 2h)
8. Add password reset flow with email service (est. 3h)
9. Add rate limiting middleware (est. 1h)
10. Write unit tests for all auth endpoints (est. 4h)
11. Write integration tests for OAuth flows with mocked providers (est. 3h)

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| JWT secret leak | Low | Store in env var, rotate quarterly, use RS256 for production |
| OAuth provider downtime | Low | Graceful fallback to email login, retry with backoff |
| Brute-force attacks | Medium | Rate limiting + account lockout after 10 failed attempts |
| Token replay attacks | Low | Short-lived access tokens + refresh rotation |

## Decisions
| Decision | Rationale | Date |
|---|---|---|
| JWT over sessions | Stateless scaling for horizontal deployment | 2025-01-15 |
| RS256 over HS256 | Asymmetric keys allow public verification without secret sharing | 2025-01-16 |
| Refresh token rotation | Mitigates token theft — each refresh invalidates the previous | 2025-01-16 |
| bcrypt over argon2 | Wider library support; sufficient for current threat model | 2025-01-15 |

## Outcome
- **Result:** All endpoints implemented and passing. 94% test coverage on auth module.
- **Metrics:** Login latency p99 = 45ms. Token refresh p99 = 12ms. Zero failed login floods in load test (500 req/s).
- **Follow-up tasks:** MFA support, admin role system, session revocation UI.
- **Reflection logged:** [2025-01-22 entry in learning/reflection-log.md]
