# AeroTwin Backend

Production infrastructure for AeroTwin's FastAPI services. Business modules should
depend on the abstractions in `repositories/`, `database/`, and `security/` rather
than framework globals.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
ENVIRONMENT=testing PYTHONPATH=backend uvicorn app.main:app --reload
```

Configuration precedence is: constructor values, environment variables, `.env`,
mounted files in `SECRETS_DIR`, environment YAML, then model defaults. YAML files
contain non-secret defaults only. Supply credentials as uppercase environment
variables (for example `DATABASE_URL`) or set `SECRETS_DIR` to a mounted directory
containing a file named after each setting. Never commit `.env` or secret files.

Production validates that debug mode and wildcard CORS are disabled. Configure
`TRUSTED_HOSTS` and `BACKEND_CORS_ORIGINS` explicitly at deployment time.

## Operational endpoints

| Endpoint | Purpose | Dependency checks |
| --- | --- | --- |
| `/liveness` | Process restart probe | None |
| `/readiness` | Traffic admission probe | Database, when configured |
| `/health` | Operator diagnostic summary | Database, when configured |

The endpoints also remain available below `/api/v1` for API clients. All API
responses use `{success, data, meta}` or `{success, error, meta}` envelopes.

## Architecture extension points

- Add ORM models on `app.database.session.Base`; Alembic reads its metadata.
- Implement bounded-context repositories by extending `AbstractRepository`.
- Coordinate writes through `SQLAlchemyUnitOfWork`; services explicitly commit.
- Implement security protocols only when authentication policy is approved.
- Future OCR, trajectory, weather, terrain, simulation, and narration packages
  should expose application ports and infrastructure adapters independently.

## Quality gates

Run from the repository root before every commit:

```bash
pytest backend/tests
ruff check backend
black --check backend
mypy backend
coverage run --source=backend/app -m pytest backend/tests
coverage report --fail-under=90
```

Database tests use mocks and do not require PostgreSQL. Migration integration tests
should run against an ephemeral PostgreSQL instance in CI once the first business
model is introduced.
