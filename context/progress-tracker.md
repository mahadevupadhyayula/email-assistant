# Progress Tracker

Update this file after every meaningful implementation change.

## Current phase

Build Unit 02 Google identity and read-only Gmail consent complete and verified.

## Current goal

Await the Unit 03 specification and explicit approval before beginning email sync.

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
- Added Google application sign-in with identity-only scopes, PKCE, state validation,
  ten-minute state expiry, verified identity binding, and automatic founder workspace creation.
- Added a separate Gmail consent disclosure and OAuth lifecycle that requests only
  Gmail read-only access plus the identity scopes required to prevent account mismatch.
- Added the workspace-scoped `GmailConnection` contract with provider identity, exact
  granted scopes, status/timestamps, encrypted credentials, and future sync cursors.
- Added Fernet token envelopes using a local environment key, renewable-token refresh,
  safe refresh-failure transitions, provider revocation, and local credential clearing.
- Added workspace-scoped consent/sign-in/disconnect audit events without token or email
  content in event metadata.
- Added responsive Gmail settings, connection health, revoked/expired states, explicit
  disconnect semantics, and a distinct data-deletion placeholder.
- Documented local Google OAuth callback configuration, scope separation, encryption-key
  handling, and the pre-hosting managed-key replacement requirement.

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

- No implementation unit is in progress.

## Next up

- Restore/provide the missing build plan and Unit 03 specification, then begin Unit 03
  only after explicit approval.

## Unit 02 acceptance evidence — 2026-10-02

- Google application sign-in and Gmail consent are separate routes, sessions, screens,
  actions, and scope sets.
- Identity authorization requests `openid`, `email`, and `profile`; mailbox consent adds
  only `https://www.googleapis.com/auth/gmail.readonly` and has no mutation scope.
- OAuth requests use state and PKCE, callbacks reject missing, mismatched, denied, or
  older-than-ten-minute state, and redirect targets are restricted to local paths.
- Gmail callback rejects signed-in/mailbox account mismatch, incomplete scope grants,
  missing renewable access, active duplicate mailbox use, and partial provider failure.
- OAuth access and refresh credentials are encrypted before persistence and cleared on
  disconnect; templates, audit metadata, and tests expose no stored secret.
- Permanent refresh-token revocation marks a connection expired; transient refresh failures
  retain encrypted credentials for retry, and revoked and expired states render visibly.
- Workspace-scoped managers and authorization tests prevent cross-workspace connection access.
- Disconnect attempts provider revocation, preserves a reversible connection record, and
  explicitly does not claim to delete previously stored email data.
- Ruff formatting and linting, strict mypy, 26 automated tests, Django system checks,
  migration drift checks, Tailwind asset compilation, and Compose validation pass.
- Tests use mocked Google boundaries. No external service, live mailbox, email sync,
  Gmail mutation, deployment, commit, push, or model call was performed.
- Malformed Google sign-in session timestamps return the controlled OAuth error response.
- Permanently revoked Gmail refresh credentials are cleared when the connection expires;
  transient provider failures retain the encrypted credential envelope and connected state.
- Gmail connections with retained credentials remain disconnectable for cleanup and revocation,
  regardless of their current connection status.
- Google sign-in redirect targets now use Django's host-and-scheme validator, including
  same-host enforcement and HTTPS downgrade protection, with regression coverage.
- Google sign-in rejects inactive users before identity binding, workspace membership,
  or audit creation while preserving the conflicting-subject response.
- Gmail consent validation now prefers Google's reported granted scopes, accepts the
  userinfo email alias, rejects unapproved scopes, and safely handles omitted grant metadata.

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

Unit 02 is a clean rollback boundary before any email import. Do not begin Unit 03
without its specification and explicit approval. The repository currently supports
Google identity and read-only Gmail authorization but has no email sync, Gmail
mutation, model calls, or deployed external runtime. `context/specs/00-build-plan.md`
is referenced by repository guidance but is currently absent and should be restored.
