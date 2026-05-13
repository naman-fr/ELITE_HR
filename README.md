# 🌿 ELITE HR Intelligence Platform v2.0

![Platform Header](https://raw.githubusercontent.com/naman-fr/ELITE_HR/main/frontend/public/preview.png)

> **The Boardroom-Ready HRMIS + AI + SecOps Suite.**  
> *Consolidate workforce data, predict employee risk, and empower your HR team with a conversational AI co-pilot—all in one premium, high-performance interface.*

---

## 🚀 Overview

ELITE HR is a production-grade Intelligence Platform designed for modern HR teams. It bridges the gap between static spreadsheets and fragmented security tools by unifying **Workforce Analytics**, **Identity Management**, and **Security Telemetry** into a single, AI-powered dashboard.

### 💎 Key Pillars
- **🧠 Hybrid AI Co-pilot**: Powered by Groq (Llama 3.1) or OpenAI (GPT-4o), capable of complex HR reasoning with full context from your datasets.
- **📊 Real-time Analytics**: Live workforce KPIs, attrition trends, and department-level productivity metrics.
- **🛡️ SecOps Intelligence**: Integrated monitoring of device health (Wazuh) and identity security (Keycloak MFA).
- **🔄 Universal Excel Transformer**: Intelligent ingestion layer that maps any Excel format to the platform's master specification.

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS (Custom Premium Theme) |
| **Backend** | FastAPI (Python 3.11), Uvicorn |
| **AI Engine** | Groq (Llama 3.1 70B) / OpenAI (GPT-4o) |
| **Vector Store** | ChromaDB (Persistent Local Storage) |
| **Security** | Wazuh XDR Integration, Keycloak IAM |
| **Deployment** | Docker & Docker Compose |

---

## ⚡ Quick Start

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- An API Key from [Groq](https://console.groq.com/) or [OpenAI](https://platform.openai.com/).

### 2. Environment Configuration
Clone the repository and create your `.env` file:
```bash
cp .env.example .env
```
Edit `.env` and provide your API keys:
```env
OPENAI_API_KEY=gsk_your_groq_key_here  # Groq and OpenAI keys are both supported!
WAZUH_API_KEY=your_key
KEYCLOAK_TOKEN=your_token
```

### 3. Launch the Platform
Run the following command to build and start the entire stack:
```bash
docker-compose up --build -d
```

---

## 🖥️ Accessing the Platform

Once the containers are running, you can access the platform via your browser:

- **🌐 Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **🔌 Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 📂 Using Your Data
1. Navigate to the **Settings** tab.
2. Use the **Universal Excel Transformer** to upload your existing employee spreadsheets.
3. The platform will automatically map your columns and refresh the entire dashboard in real-time.

---

## 🧠 AI Co-pilot Capabilities
The ELITE HR Co-pilot isn't just a chatbot; it's a strategic partner. You can ask:
- *"Who are our highest flight risks in Engineering this quarter?"*
- *"Show all orphaned accounts from the last offboarding cycle."*
- *"Draft a Performance Improvement Plan (PIP) for Employee X based on their productivity dip."*
- *"Which employees have not yet enrolled in MFA?*

---

## 📜 License
Internal Engineering Use | © 2026 ELITE HR Technologies.

---
*Built with ❤️ for Global HR Teams.*
