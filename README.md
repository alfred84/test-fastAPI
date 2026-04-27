# test-fastAPI

Backend for Frontend (BFF) built with FastAPI that proxies React requests to External API, persists sessions, and audits mutable client operations.

## Tech Stack

- Python 3.13
- FastAPI + Uvicorn
- MongoDB + Motor + Beanie
- HTTPX async client
- Pydantic Settings
- Pytest + pytest-asyncio

## Architecture

```
app/
  core/          # config, dependencies, security, exceptions, logging
  domain/        # pure entities and business models
  schemas/       # request/response DTOs
  repositories/  # Beanie documents + persistence abstractions
  services/      # use-case orchestration and external API adapter
  routers/       # thin controllers (FastAPI endpoints)
```

## Environment Variables

Copy `.env.example` to `.env` and adjust:

- `MONGODB_URL`
- `EXTERNAL_API_URL`
- `PORT`
- `APP_ENV`
- `CORS_ALLOWED_ORIGINS`
- `HTTPX_TIMEOUT_SECONDS`
- `HTTPX_RETRY_ATTEMPTS`
- `HTTPX_RETRY_BACKOFF_MS`
- `SESSION_TTL_HOURS`

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

### Auth
- `POST /auth/login`
- `POST /auth/logout`

### Clients
- `POST /clients/list`
- `POST /clients/create`
- `PUT /clients/update`
- `DELETE /clients/{id}`
- `GET /clients/{id}`

## Testing (TDD)

```bash
pytest
```

Recommended flow:
1. Write failing endpoint test.
2. Write failing service test.
3. Implement minimal code.
4. Refactor with tests green.

## Docker

```bash
docker compose up --build
```

Services:
- API: `http://localhost:${PORT}`
- MongoDB: `mongodb://localhost:27017`

## Render Deployment

1. Create Render Web Service connected to repository.
2. Set environment variables from `.env.example`.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Confirm `/health` responds with `{"status":"ok"}`.

## Git Strategy

- Use feature branches (e.g. `feat/auth-login-logout`, `feat/clients-bff-crud`).
- Use conventional commits:
  - `feat(auth): implement login proxy`
  - `feat(clients): add client CRUD endpoints`
  - `fix(session): correct token persistence`
- Keep commits atomic: one coherent change plus related tests.
