# User Management API (FastAPI)

Production-grade User Management API implementing registration, JWT login, profile access,
RBAC-protected user retrieval, and paginated user listing.

## Tech Stack
- FastAPI
- SQLAlchemy 2.0 (sync engine)
- JWT auth via `python-jose`
- Password hashing via `passlib[bcrypt]`
- Alembic migrations
- Pytest test suite
- Optional rate limiting via `slowapi`
- Dockerfile + docker-compose
- Ruff lint & GitHub Actions CI

## Setup
- Python 3.10+
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` as needed.

## Run
```bash
uvicorn app.main:app --reload
```

## Env Vars
- `DATABASE_URL`
- `JWT_SECRET`
- `ACCESS_TOKEN_EXPIRES_MIN`

## DB Init / Migrations
```bash
alembic upgrade head
python scripts/seed_admin.py  # creates an initial admin if not exists
```

## Example Requests
```bash
# Register
http POST :8000/users name=Alice email=alice@example.com password=Str0ng!Pass

# Login
http POST :8000/login email=alice@example.com password=Str0ng!Pass

# Use token
http GET :8000/me "Authorization:Bearer <token>"

# Get own user by id (or any user if admin)
http GET :8000/users/<uuid> "Authorization:Bearer <token>"

# List users (admin only)
http GET ':8000/users?page=1&limit=20' "Authorization:Bearer <token>"
```

## Tests
```bash
pytest -q
```

## Docker
```bash
docker compose up --build
```

## CI
GitHub Actions runs `ruff` and `pytest` on PRs.

---

**Notes & Trade-offs**
- Sync SQLAlchemy chosen for simplicity and reliability with FastAPI. Can be flipped to async if needed.
- Basic rate limiting configured for `/login`. Consider central cache or IP-awareness for distributed setups.
