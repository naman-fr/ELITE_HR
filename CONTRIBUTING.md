# Contributing to ELITE HR

Thank you for contributing to the ELITE HR Intelligence Platform. This guide covers local development, testing, and pull request expectations.

## Development setup

### Prerequisites

- Docker Desktop (recommended) or Python 3.11 + Node.js 20
- Groq or OpenAI API key

### Quick start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

For Hugging Face / single-container parity:

```bash
docker compose --profile unified up --build app
```

### Local backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Local frontend

```bash
cd frontend
npm ci
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## Testing

```bash
cd backend && pytest -q
cd frontend && npm run lint && npm run build
```

CI runs the same checks on every push to `main`.

## Code standards

- **Backend:** Ruff for linting, type hints where practical, structured logging
- **Frontend:** ESLint + TypeScript, shared API client in `src/lib/api.ts`
- **Commits:** Use clear, imperative messages (e.g. `Add Wazuh status endpoint`)

## Pull requests

1. Fork and create a feature branch from `main`
2. Keep changes focused and include tests for new backend behavior
3. Ensure CI passes before requesting review
4. Update `.env.example` and README when adding configuration

## Security

- Never commit `.env` files or API keys
- Report security issues privately to the repository owner
