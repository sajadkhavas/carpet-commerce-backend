# Carpet Commerce Backend

Production-oriented, white-label backend for a carpet e-commerce platform.

## Stack

- Python 3.13
- Django 5.2 LTS
- Django REST Framework
- PostgreSQL 17
- Redis
- Celery
- drf-spectacular / OpenAPI
- pytest + Ruff
- Docker Compose
- GitHub Actions

## Local development

```bash
cp .env.example .env
docker compose up --build
```

Then run migrations:

```bash
docker compose exec api python manage.py migrate
```

Endpoints:

- `GET /health/` — process health; does not depend on external services.
- `GET /ready/` — readiness; verifies database and cache connectivity.
- `GET /api/schema/` — OpenAPI schema.
- `GET /api/docs/` — Swagger UI.
- `/admin/` — Django administration.

## Development without Docker

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

For local non-Docker execution, update `DATABASE_URL`, `REDIS_URL`, and Celery URLs in `.env`.

## Engineering rules

1. `main` is release/integration truth; phase work happens on dedicated branches.
2. Secrets are environment-only and must never be committed.
3. Frontend input is never authoritative for price, inventory, payment, or order state.
4. Database changes must be represented by migrations.
5. A phase is not complete until tests and CI are green and the phase record is updated.
6. API changes must preserve or intentionally version the OpenAPI contract.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/ROADMAP.md`](docs/ROADMAP.md).
