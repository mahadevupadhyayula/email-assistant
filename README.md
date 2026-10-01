# Email Assistant

A locally hosted, Python-first Inbox Command Center for early-stage founders. Planning is complete and Build Unit 01, the local foundation, is in progress.

Start with:

- [`context/project-overview.md`](context/project-overview.md)
- [`context/architecture.md`](context/architecture.md)
- [`context/specs/00-build-plan.md`](context/specs/00-build-plan.md)
- [`context/progress-tracker.md`](context/progress-tracker.md)

## Local setup

The current scaffold requires Python 3.12, [uv](https://docs.astral.sh/uv/), and Node.js.

```bash
cp .env.example .env
uv sync
npm install
uv run python manage.py check
```

Replace the placeholder `DJANGO_SECRET_KEY` in `.env` with a unique local value. Local environment files, virtual environments, installed JavaScript packages, databases, caches, and build output are excluded from Git.

Build Unit 01 is not complete yet. Follow [`context/specs/01-local-foundation.md`](context/specs/01-local-foundation.md) and the status in [`context/progress-tracker.md`](context/progress-tracker.md).
