---
title: HR Board
emoji: 🌿
colorFrom: green
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🌿 ELITE HR Intelligence Platform v2.1

![Platform Header](frontend/public/preview.png)

> **The Boardroom-Ready HRMIS + AI + SecOps Suite.**  
> Consolidate workforce data, predict employee risk, and empower your HR team with a conversational AI co-pilot—all in one premium, high-performance interface.

---

## Overview

ELITE HR is an industrial-grade HR intelligence platform that unifies **Workforce Analytics**, **Identity Management (Keycloak)**, and **Security Telemetry (Wazuh XDR)** with a Task-Oriented Dialogue (TOD) AI co-pilot.

### Key capabilities

| Pillar | Description |
|--------|-------------|
| **Hybrid AI Co-pilot** | Groq (`llama-3.3-70b-versatile`) or OpenAI (`gpt-4o`) with ChromaDB RAG |
| **Real-time Analytics** | Live headcount, productivity, department distribution |
| **SecOps Intelligence** | Wazuh endpoint monitoring + Keycloak MFA compliance |
| **Universal Data Transformer** | Excel/CSV ingestion mapped to the master HR schema |

---

## Technology stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 16 (App Router), React 19, TypeScript, custom CSS design system |
| **Backend** | FastAPI, Pydantic Settings, Uvicorn, SlowAPI rate limiting |
| **AI Engine** | Groq / OpenAI with ChromaDB vector store |
| **Security** | Wazuh XDR, Keycloak IAM (live API + Excel simulation fallback) |
| **Deployment** | Docker Compose, Hugging Face Spaces (unified container) |
| **Quality** | GitHub Actions CI, pytest, Ruff, ESLint |

---

## Quick start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Groq or OpenAI API key

### 1. Configure environment

```bash
git clone https://github.com/naman-fr/ELITE_HR.git
cd ELITE_HR
cp .env.example .env
```

Edit `.env` and set at minimum:

```env
OPENAI_API_KEY=gsk_your_groq_key_here
```

### 2. Launch (split stack — recommended for local dev)

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:3000 |
| API docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |

### 3. Launch (unified — Hugging Face parity)

```bash
docker compose --profile unified up --build app
```

Access at http://localhost:7860

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health and configuration summary |
| `GET` | `/stats` | Workforce KPIs from master Excel |
| `GET` | `/wazuh/status` | Endpoint security status (live or simulation) |
| `GET` | `/keycloak/status` | IAM/MFA compliance (live or simulation) |
| `GET` | `/compliance/alerts` | Active compliance alerts |
| `POST` | `/upload` | Transform and ingest Excel/CSV |
| `POST` | `/chat` | AI co-pilot (rate-limited) |
| `POST` | `/ingest` | Re-index master data into ChromaDB |

---

## Using your data

1. Open the **Settings** tab in the dashboard.
2. Upload `.xlsx` or `.csv` employee data.
3. The Universal Excel Transformer maps columns to the master schema.
4. Dashboard metrics and the AI co-pilot refresh automatically.

---

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, testing, and PR guidelines.

```bash
# Backend tests
cd backend && pytest -q

# Frontend lint + build
cd frontend && npm run lint && npm run build
```

---

## AI co-pilot examples

- *"Who are our highest flight risks in Engineering this quarter?"*
- *"Show all orphaned accounts from the last offboarding cycle."*
- *"Which employees have not yet enrolled in MFA?"*
- *"Draft a PIP for Employee X based on their productivity dip."*

---

## License

[MIT License](LICENSE) — © 2026 ELITE HR Technologies

Built for global HR teams. 🌿
