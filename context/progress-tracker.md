# Progress Tracker

Update this file after every meaningful implementation change.

## Current phase

Build Unit 01 local foundation complete and verified.

## Current goal

Await approval to begin Build Unit 02: Google identity and read-only Gmail consent.

## Completed

- Defined primary user, problem, product progression, and MVP boundary.
- Defined measurable success criteria.
- Defined dashboard, briefing, chat, priority, confidence, and correction behavior.
- Selected Gmail-only scope and ten-day active-thread import rule.
- Selected 90-day thread-level retention.
- Selected multi-tenant foundation with single-user visible MVP.
- Selected Python/Django/LangGraph/LangChain architecture.
- Selected OpenAI as MVP provider behind a model-agnostic capability interface.
- Selected local hosting and documented future AWS direction.
- Created build plan, feature specs, and recording plan.
- Initialized the Python 3.12/Django 5.2 project scaffold and dependency locks.
- Added repository ignore rules and environment-based Django secret, debug, and host configuration.
- Documented the initial local setup and stable Django check command.
- Added environment-specific Django settings, ASGI and Celery configuration.
- Added Docker Compose services for PostgreSQL, Redis, web, worker, and scheduler,
  with observable health and migration-gated startup.
- Configured Django cache to use Redis DB 1 separately from the Celery broker in
  Redis DB 0, including Compose and local environment defaults.
- Added the custom `User`, `Workspace`, and future-compatible `Membership` role
  models plus the initial migration.
- Established an explicit workspace-scoped manager and tenant-isolation tests.
- Added an idempotent, debug-only development account bootstrap command.
- Added authenticated local sign-in and a responsive, keyboard-accessible empty
  command-center shell with three lenses and an assistant placeholder.
- Bound the mobile workspace switch's active styling and pressed state to the
  displayed panel so its selection is correct on load and after clicks.
- Added liveness and database/Redis readiness endpoints.
- Readiness now returns HTTP 503 and a top-level unavailable status when the
  Redis healthcheck read does not return its expected value.
- Added stable asset-build, formatting, linting, typing, test, migration, and
  Compose validation commands to the README.
- Verified 11 automated tests, Ruff formatting/linting, strict mypy, Django checks,
  migration consistency, frontend asset build, and Compose configuration.
- Verified fresh Docker startup: PostgreSQL, Redis, ASGI web, Celery worker, and
  Celery Beat report healthy; migrations exit successfully; readiness reports
  database and Redis healthy; repeated development bootstrap remains idempotent.
- Verified the live browser flow: authentication redirects correctly, local sign-in
  succeeds, the compiled responsive shell renders with its intended styling, lens
  selection updates accessibly, and keyboard navigation reaches the skip link first.
- Added WhiteNoise static delivery and build-time static collection after the live
  ASGI browser check exposed and verified the missing-asset failure mode.

## Unit 01 acceptance evidence — 2026-10-01

- Fresh Docker Compose build and startup completed successfully.
- PostgreSQL, Redis, Django ASGI web, Celery worker, and Celery Beat reported healthy.
- The migration service completed successfully with exit code 0.
- `/health/live/` returned HTTP 200.
- `/health/ready/` returned HTTP 200 with database and Redis marked `ok`.
- Development account bootstrap succeeded twice without creating duplicates.
- Workspace ownership, membership uniqueness, tenant scoping, authentication,
  dashboard rendering, and dependency failure behavior are covered by 12 passing tests.
- Ruff formatting and linting, strict mypy, Django system checks, migration drift
  checks, Tailwind asset compilation, and Docker Compose validation passed.
- Chrome verification confirmed the styled desktop shell, successful local sign-in,
  accessible lens selection, and skip-link-first keyboard navigation.
- Google OAuth, Gmail access, model calls, external writes, deployment, commits, and
  pushes were not performed.

## In progress

- Next specification: Build Unit 02 — Google identity and separate read-only Gmail
  consent. Implementation awaits explicit approval.

## Next up

- Build Unit 02 only after explicit approval: Google identity and separate read-only
  Gmail consent.

## Open questions

- Exact OpenAI model after capability evaluation
- Local token-encryption and developer key workflow
- SSE versus WebSockets for streamed chat
- Final branding and visual tokens
- Future AWS region, RPO, and RTO

## Product and architecture decisions

- MVP is an Inbox Command Center for early-stage founders.
- Morning briefing and chat are both primary experiences.
- Founder-defined priorities drive importance.
- Ranking is structured AI extraction plus deterministic rules.
- Gmail access remains read-only throughout MVP.
- Local Docker Compose is the MVP runtime.
- AWS deployment is future work only.

## Risks and blockers

- Gmail OAuth verification and scopes may affect later external distribution.
- Ten days of activity may be insufficient for relationship inference; guided priorities mitigate this.
- LLM extraction quality must be measured with controlled fixtures before relying on rankings.
- Retaining normalized email requires careful deletion lineage and secret handling.
- A model-agnostic interface can become lowest-common-denominator abstraction if capabilities are not explicit.

## Resume notes

Unit 01 is a clean rollback boundary before external identity or mailbox data. Do
not begin Unit 02 without explicit approval. The current local runtime has no
Google OAuth, Gmail access, model calls, or external writes.
