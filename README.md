# Yotta Flextator API

Production-ready FastAPI backend scaffold for an AI-powered career mentoring platform.

## Tech stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic schemas
- Environment-based application configuration
- Clean architecture style separation for routers, services, schemas, and models

## Folder structure

```text
career-mentor-api/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   ├── router.py
│   │   └── v1/endpoints/
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── .env.example
├── requirements.txt
└── README.md
```

## Supported roles

- Employee
- Manager
- HR
- Organization

## Core feature modules

- User profile management
- AI career roadmap generation
- Skill gap analysis
- Learning recommendations
- Chat assistant
- Manager dashboard
- HR analytics
- Organization insights

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

## Environment variables

```env
APP_NAME=Yotta Flextator API
APP_ENV=development
APP_DEBUG=true
API_V1_PREFIX=/api/v1
CORS_ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Database migrations

Alembic is the source of truth for schema changes. The application and Alembic both read the database URL from `app/db/session.py`.

Update `MAIN_DATABASE_URL` in `app/db/session.py` to match your local or deployed PostgreSQL credentials before starting the app or running migrations.

```bash
# apply all pending migrations
alembic upgrade head

# create a new migration after changing SQLAlchemy models
alembic revision --autogenerate -m "describe the change"

# review the generated file in alembic/versions/

# apply the new revision locally
alembic upgrade head
```

### Recommended workflow

1. Change the SQLAlchemy models.
2. Generate a migration with `alembic revision --autogenerate -m "describe the change"`.
3. Review the generated revision carefully, especially destructive operations and server defaults.
4. Apply it locally with `alembic upgrade head`.
5. Run `python -m app.db.seed` if your change depends on default reference data.
6. Smoke-test the app before committing.

### Useful commands

```bash
# show the current applied revision
alembic current

# list migration history
alembic history

# roll back one migration
alembic downgrade -1

# roll back to a specific revision
alembic downgrade <revision_id>

# mark an existing database as already being at the latest revision
alembic stamp head
```

For a brand-new local database, always run `alembic upgrade head` before starting the API. Do not rely on ad hoc `create_all()` table creation in development or production.

If you need a programmatic bootstrap path, `app.db.session.init_db()` applies migrations with `alembic upgrade head`.

## Database seeding

Run the seed script only after migrations have completed successfully.

```bash
alembic upgrade head
python -m app.db.seed
```

The seeding script is idempotent:

- missing default roles are inserted
- missing designations are inserted
- the default HR user is created once and reused on later runs
- rerunning the script does not create duplicate rows

Default seed data includes:

- roles: Admin (`organization_admin`), HR (`hr`), and Employee (`employee`)
- designation hierarchy: Associate L1, Associate L2, Senior Associate, Lead, Senior Lead, Assistant Manager, Manager, Senior Manager, Associate Director, Director, Senior Director, Vice President
- default user: `hr.manager@career-mentor.local` with role `hr` and designation `Manager`

The seed user is created with the password `ChangeMe123!`. Change it immediately if you use the account outside local setup. If the user already exists, rerunning the seed script preserves the existing password.

## Notes

- The project models target PostgreSQL in development and production.
- The test suite uses SQLite, with compatibility shims for PostgreSQL-specific column types.

## User listing API

`GET /api/v1/users` returns all users with `first_name`, `last_name`, `role`, `designation`, and `status`.

- Access is restricted to `organization_admin` and `hr` users.
- The endpoint uses the authenticated Cognito user from the `Authorization: Bearer <token>` header.
- For local development without Cognito configured, you can pass `X-User-Id: <user-uuid>` instead.
- The response returns an empty list when no users exist.

## User creation API

`POST /api/v1/users` accepts either `role` or `role_id`, keeps `manager_id` optional, creates the user in Cognito, and then stores the same Cognito `sub` as the local `users.id`.

- `designation_id` is required.
- `manager_id` may be omitted or set to `null`.
- Cognito admin creation requires valid AWS credentials plus `COGNITO_REGION` and `COGNITO_USER_POOL_ID`.
