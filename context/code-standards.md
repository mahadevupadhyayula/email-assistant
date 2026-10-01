# Code Standards

## General

- Use supported Python and Django releases selected at project initialization and pin dependencies with a lock file.
- Prefer a modular monolith with domain-oriented Django apps.
- Keep views thin; place business behavior in typed application services.
- Do not introduce another framework, queue, database, or model abstraction without an approved architecture change.

## Python and typing

- Use `snake_case` for functions/modules, `PascalCase` for classes, and explicit domain names over generic helpers.
- Type public functions, service methods, task inputs, and adapter contracts.
- Use Pydantic models for model-provider input/output contracts; use Django models for persistence.
- Avoid passing unvalidated dictionaries across domain boundaries.
- Make time-zone handling explicit and store timestamps in UTC.

## Django boundaries

- Every tenant-owned model includes a required workspace relationship.
- All application queries use workspace-scoped managers/repositories.
- Views/forms validate user input; services enforce authorization and invariants again.
- Keep provider IDs and provider payload handling inside integration modules.
- Use migrations for every schema change; never edit applied migrations casually.
- Use Django admin only for controlled operational inspection, not as the founder experience.

## AI and LangGraph

- Product-owned schemas and capability protocols must not expose provider SDK objects.
- Graph nodes perform one named responsibility and return typed state updates.
- Separate deterministic preprocessing, model calls, validation, ranking, and persistence.
- Version prompts, schemas, graph definitions, and ranking rules.
- Never let free-form model prose directly perform a database mutation.
- Tool handlers enforce authorization and validate arguments independently of the model.
- Tests use fake adapters by default; live model tests are separately marked and budgeted.

## Celery

- Task payloads contain stable IDs, not email bodies or serialized ORM objects.
- Tasks are idempotent or explicitly document why they cannot be.
- Configure bounded retries with backoff for transient failures.
- Do not wait synchronously for subtasks inside workers.
- Record task run state and use correlation IDs.
- Keep one logical periodic scheduler active.

## Validation and errors

- Use domain-specific exceptions and map them to safe user-facing states.
- Distinguish validation, authorization, provider, rate-limit, transient, and permanent errors.
- Never swallow failures that can make a briefing incomplete.
- Display stale/partial states with last-success timestamps.
- Redact email content, tokens, secrets, and model prompts from error reporting.

## Logging and audit

- Emit structured logs with event name and correlation identifiers.
- Use pseudonymous workspace/user IDs in diagnostics.
- Store user-visible or security-relevant actions as audit events.
- Do not treat logs as a durable product database.

## Testing

- Unit-test ranking rules, confidence thresholds, state transitions, retention, and authorization.
- Contract-test Gmail and model adapters with sanitized fixtures.
- Integration-test Django, PostgreSQL, Redis/Celery boundaries, and migrations.
- Test every workspace query for tenant isolation.
- Use controlled synthetic email scenarios for AI evaluations.
- End-to-end test onboarding, sync, briefing, tabs, chat, correction, and deletion.
- Require regression examples for every corrected AI failure.

## UI and accessibility

- Use semantic HTML before custom widgets.
- All actions are keyboard reachable and have visible focus.
- Never encode importance, urgency, or confidence by color alone.
- HTMX responses must preserve accessible focus and announce meaningful updates.
- Provide loading, empty, partial, stale, error, and needs-review states.
- Keep mobile layouts usable at narrow widths without horizontal scrolling.

## Secrets and dependencies

- Secrets come from local environment configuration and never enter source control.
- Provide a safe example environment file with placeholders only.
- Prefer maintained dependencies with a clear, necessary role.
- Record security-sensitive dependency decisions.
- Run dependency and image checks before any hosted release.

## Verification commands

Exact commands will be finalized during project initialization. The project must provide stable commands for formatting, linting, type checking, unit tests, integration tests, migrations, AI evaluations, and local end-to-end verification. Document them in the README and CI when introduced.

