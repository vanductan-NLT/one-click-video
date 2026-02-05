# One Click Video - Developer Guide (M0.1)

Welcome to the **One Click Video** project! This document will help you get started with the local development environment.

## 🚀 Quick Start

### 1. Prerequisites
- Docker & Docker Compose
- WSL2 (if on Windows)
- Python 3.11+ (for local IDE support)

### 2. Setup Environment
```bash
cp .env.example .env
# Update .env with your local settings if needed
```

### 3. Spin up Infrastructure
```bash
docker compose -f docker-compose.dev.yml up -d
```
This will start:
- **API**: http://localhost:8000
- **pgAdmin**: http://localhost:5050 (Credentials: admin@admin.com / admin)
- **Redis**: port 6379
- **Postgres**: port 5432

### 4. Running Migrations
```bash
# Inside API container
docker compose -f docker-compose.dev.yml exec api alembic revision --autogenerate -m "initial"
docker compose -f docker-compose.dev.yml exec api alembic upgrade head
```

---

## 🏗 Architecture: Modular Monolith

We follow a **Modular Monolith** pattern with **Clean Architecture** within each module.

### Directory Structure
- `src/api/`: Global API registration and entry point.
- `src/modules/`: Business modules (video_processing, etc.)
    - `domain/`: Pure business logic (Entities, Value Objects). **No dependencies**.
    - `application/`: Orchestration and Use Cases (Handlers).
    - `infrastructure/`: Technical details (DB Repositories, External Adapters).
    - `api/`: Module-specific routes.
- `src/shared/`: Shared utilities, config, and database core.
- `src/worker/`: Celery worker and background tasks.

### Coding Rules
1. **Dependency Direction**: Inward only (`Infrastructure -> Application -> Domain`).
2. **Persistence**: Never leak SQLAlchemy models into Domain or Application. Use Domain Entities.
3. **Async**: Use `async/await` for all I/O bound operations (DB, API).

---

## 🧪 Testing

We use `pytest`.

```bash
# Run all tests
pytest
```

- **Unit tests**: `tests/unit/` (Fast, no external dependencies).
- **Integration tests**: `tests/integration/` (Tests API and DB interaction).

---

## 🛠 Useful Commands

| Command | Description |
|---------|-------------|
| `docker compose -f docker-compose.dev.yml logs -f api` | Follow API logs |
| `docker compose -f docker-compose.dev.yml exec api uvicorn ...` | Restart uvicorn |
| `alembic history` | View migration history |
