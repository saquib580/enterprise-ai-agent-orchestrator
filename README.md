# Enterprise AI Agent Orchestrator

A Python 3.12 / FastAPI starter repository for an enterprise multi-tenant AI agent orchestration platform.

## Included
- FastAPI application factory, health route and versioned simulated agent endpoint.
- Pydantic Settings v2 configuration.
- SQLAlchemy 2 async engine and aiomysql session dependency.
- Timestamp and tenant-scoping ORM mixins.
- Agent model and generic tenant-aware repository.
- Ruff, mypy, pytest and GitHub Actions CI.
- Product overview and 90-day daily engineering plan in `docs/`.

The agent endpoint is a non-blocking simulation. It does not call an LLM, persist an execution or provide production authentication. The ORM schema is not automatically created on startup.

## Requirements
Ubuntu 22.04+ or equivalent, Python 3.12, Git and GNU Make. MySQL 8+ is needed for database-backed development.

## Quick start
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-ai-agent-orchestrator
cp .env.example .env
python3.12 -c "import secrets; print(secrets.token_urlsafe(48))"
# Put the generated value in SECRET_KEY in .env.
make install-dev
make run
```

Open http://127.0.0.1:8000/docs and http://127.0.0.1:8000/health.

Try the simulation:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/agent/execute \
  -H 'Content-Type: application/json' \
  -d '{"tenant_id":1,"agent_id":1,"prompt":"Review a sample function"}'
```

## Quality commands
```bash
make test
make lint
make format
make typecheck
make check
```

## MySQL setup
```sql
CREATE DATABASE enterprise_ai_orchestrator
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'enterprise_app'@'localhost' IDENTIFIED BY 'replace-with-a-strong-password';
GRANT SELECT, INSERT, UPDATE, DELETE
  ON enterprise_ai_orchestrator.* TO 'enterprise_app'@'localhost';
FLUSH PRIVILEGES;
```
Set matching values in `.env`. Use a separate migration identity with DDL privileges when migrations are introduced.

## Push to GitHub
```bash
git init
git add .
git status
git commit -m "chore: initialize enterprise AI agent orchestrator"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Never commit `.env`, API keys, passwords or private keys.

## Production boundary
Before production use, implement authenticated tenant identity and authorization, mandatory tenant scoping on every access path, versioned migrations, durable execution records/checkpoints, model-provider integration, rate limiting, audit logging, secrets management, observability, backup/restore and deployment hardening. A tenant ID supplied in the demo request is illustrative, not authorization.

Yoyo migration execution should run as a controlled deployment operation, not inside an async request. Application DB access uses SQLAlchemy async sessions.

## Repository layout

```text
enterprise-ai-agent-orchestrator/
├── .github/workflows/backend-ci.yml
├── backend/
│   ├── app/api/v1/agents.py
│   ├── app/core/config.py
│   ├── app/db/{base.py,session.py}
│   ├── app/models/agent.py
│   ├── app/repositories/base.py
│   ├── app/main.py
│   ├── requirements/{base.txt,dev.txt}
│   ├── tests/test_health.py
│   ├── main.py
│   └── pyproject.toml
├── docs/
│   ├── PRODUCT_OVERVIEW_AND_ARCHITECTURE.md
│   └── High-Level%20Architecture.png
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── Makefile
└── README.md
```
