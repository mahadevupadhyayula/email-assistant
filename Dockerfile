FROM node:22-alpine AS assets
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY assets ./assets
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir uv==0.9.18
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev
COPY . .
COPY --from=assets /app/dashboard/static/dist ./dashboard/static/dist
COPY --from=assets /app/dashboard/static/vendor ./dashboard/static/vendor
RUN .venv/bin/python manage.py collectstatic --noinput
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
