# Email Assistant

A locally hosted, Python-first Inbox Command Center for early-stage founders. Build
Unit 01 provides the local, workspace-scoped application foundation.

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

Unit 01 intentionally contains no Google OAuth, Gmail access, or model calls. Follow
[`context/progress-tracker.md`](context/progress-tracker.md) for the next approved unit.
