# Email Assistant

A locally hosted, Python-first Inbox Command Center for early-stage founders. Build
Units 01–02 provide the local foundation, Google identity, and a separate read-only
Gmail consent lifecycle. Email sync is not implemented yet.

Start with:

- [`context/project-overview.md`](context/project-overview.md)
- [`context/architecture.md`](context/architecture.md)
- [`context/specs/00-build-plan.md`](context/specs/00-build-plan.md)
- [`context/progress-tracker.md`](context/progress-tracker.md)

## Local setup with Docker

Docker Compose runs PostgreSQL, Redis, the Django ASGI web process, a Celery worker,
and Celery Beat. The `.env` file is optional for initial startup, but creating one
with a unique development secret is strongly recommended.

```bash
cp .env.example .env
docker compose up --build -d
docker compose run --rm web python manage.py bootstrap_dev \
  --username founder --password local-founder
docker compose ps
```

Open <http://localhost:8000>, sign in with the development credentials from the
bootstrap command, and replace the example password immediately if the local
environment is shared. Running the bootstrap command again is safe.

## Google OAuth configuration

Create a Google OAuth web client and add these exact local redirect URIs:

- `http://localhost:8000/accounts/google/callback/`
- `http://localhost:8000/gmail/callback/`

Set `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, and a local Fernet key
in `.env`. Generate the key once and keep it stable; changing it makes stored token
envelopes unreadable:

```bash
uv run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Google sign-in requests only `openid`, `email`, and `profile`. The later Connect
Gmail action is separate and requests `gmail.readonly` plus identity scopes needed
to prevent account mismatch. Credentials are encrypted in the database. Disconnect
attempts provider revocation, clears the local token envelope, and does not delete
stored inbox data. The local Fernet key is an MVP strategy intended for replacement
by managed key storage before hosted deployment.

Service health is visible through `docker compose ps`. Django exposes liveness at
`/health/live/` and database/Redis readiness at `/health/ready/`. Startup fails
visibly when migrations or required services are unavailable.

## Local development without containers

Python 3.12, [uv](https://docs.astral.sh/uv/), Node.js, PostgreSQL, and Redis are
required. Point `DATABASE_URL` and `REDIS_URL` in `.env` at those local services.

```bash
uv sync --frozen
npm ci
npm run build
uv run python manage.py migrate
uv run python manage.py bootstrap_dev
uv run uvicorn config.asgi:application --reload
```

## Stable verification commands

```bash
npm run check
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
docker compose config --quiet
```

Tests use an isolated in-memory SQLite database; the Docker runtime and integration
topology use PostgreSQL. Local environment files, virtual environments, installed
JavaScript packages, databases, caches, and build output are excluded from Git.

Unit 02 intentionally performs no email import, Gmail mutation, or model call. Follow
[`context/progress-tracker.md`](context/progress-tracker.md) for the next approved unit.
