# 01 — Local Foundation

## 1. Goal

Create a reproducible Python/Django modular-monolith foundation with workspace-scoped identity and local supporting services.

## 2. User-visible outcome

A founder can open a local responsive application, sign into a development account, and see an empty command-center shell. No Gmail or AI behavior exists yet.

## 3. Scope and exclusions

Include Django, PostgreSQL, Redis, Celery, Celery Beat, ASGI, templates, HTMX, minimal Alpine.js, Tailwind, health checks, environment configuration, and initial workspace/user/membership models. Exclude Google OAuth, Gmail, model calls, and production cloud deployment.

## 4. Design and interaction behavior

Render the calm executive shell, navigation, empty briefing state, three disabled/empty lenses, and assistant placeholder. Make desktop and narrow mobile layouts usable.

## 5. Implementation details

- Establish domain-oriented Django apps and settings by environment.
- Add Docker Compose services for web, PostgreSQL, Redis, worker, and scheduler.
- Provide safe local development authentication only if Google sign-in is not yet available.
- Add workspace-scoped managers/services and forbid convenient global tenant access.
- Establish formatting, linting, typing, testing, and migration commands.

## 6. Data, API, and state contracts

Create `Workspace`, `User` integration, and `Membership` with future-compatible roles. Every later tenant entity must reference `Workspace`.

## 7. Error and edge cases

Handle unavailable database/Redis, unapplied migrations, duplicate development setup, and worker startup without hiding failure.

## 8. Dependencies

Approved planning context only.

## 9. Security and privacy

No real email secrets in repository or fixtures. Use placeholder environment examples. Ensure debug behavior is local-only.

## 10. Test and verification checklist

- [ ] Fresh local startup succeeds from documented steps.
- [ ] Web, database, Redis, worker, and scheduler health is observable.
- [ ] Workspace model and membership tests pass.
- [ ] Cross-workspace query tests establish the base pattern.
- [ ] Responsive shell and keyboard navigation are checked.
- [ ] Formatting, linting, typing, and tests have stable commands.

## 11. Code walkthrough points

Module boundaries, workspace scope, process topology, configuration, and why local runtime remains AWS-independent.

## 12. Recording assets

One modular-monolith diagram, local process diagram, startup demonstration, and responsive shell capture.

