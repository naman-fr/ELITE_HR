from __future__ import annotations

import logging
import os
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

import excel_transformer
import rag_engine
from config import Settings, get_settings
from logging_config import configure_logging
from schemas import HealthResponse, QueryRequest
from services.wazuh import get_wazuh_status

configure_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=[])

ALLOWED_UPLOAD_EXTENSIONS = {".xlsx", ".xls", ".csv"}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Production-grade HR intelligence API with AI co-pilot and SecOps integrations."
        ),
    )
    app.state.settings = settings
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.debug("%s %s", request.method, request.url.path)
        response = await call_next(request)
        return response

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    def health_check() -> HealthResponse:
        excel_path = settings.resolve_master_excel()
        return HealthResponse(
            status="ok",
            service=settings.app_name,
            version=settings.app_version,
            environment=settings.environment,
            master_data_available=excel_path.exists(),
            llm_provider="groq" if settings.is_groq else "openai",
        )

    @app.get("/stats", tags=["analytics"])
    async def get_stats():
        excel_path = settings.resolve_master_excel()
        if not excel_path.exists():
            raise HTTPException(status_code=404, detail="Master Excel file not found")
        try:
            return rag_engine.get_excel_stats(str(excel_path))
        except Exception as exc:
            logger.exception("Failed to compute stats")
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.get("/keycloak/status", tags=["secops"])
    async def get_keycloak_status():
        try:
            connected, users, error = rag_engine.get_keycloak_data()
            if connected:
                total_users = len(users)
                mfa_enabled_count = sum(1 for user in users if user.get("totp", False))
                mfa_percentage = (
                    int((mfa_enabled_count / total_users) * 100) if total_users > 0 else 100
                )
                return {
                    "status": "Connected",
                    "connected": True,
                    "total_users": total_users,
                    "mfa_compliance": mfa_percentage,
                    "users": users[:10],
                }
            return {
                "status": "Offline (Simulation Mode)",
                "connected": False,
                "error": error,
            }
        except Exception as exc:
            logger.exception("Keycloak status check failed")
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.get("/wazuh/status", tags=["secops"])
    async def get_wazuh_endpoint():
        try:
            excel_path = settings.resolve_master_excel()
            return get_wazuh_status(excel_path)
        except Exception as exc:
            logger.exception("Wazuh status check failed")
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.get("/compliance/alerts", tags=["secops"])
    async def get_compliance_alerts():
        excel_path = settings.resolve_master_excel()
        if not excel_path.exists():
            raise HTTPException(status_code=404, detail="Master Excel file not found")
        wazuh = get_wazuh_status(excel_path)
        critical = [item for item in wazuh.get("alerts", []) if item.get("risk") != "Safe"]
        return {"total": len(critical), "alerts": critical[:10]}

    @app.post("/upload", tags=["data"])
    async def upload_excel(file: UploadFile = File(...)):
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
            allowed = ", ".join(sorted(ALLOWED_UPLOAD_EXTENSIONS))
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{suffix}'. Allowed: {allowed}",
            )

        contents = await file.read()
        if len(contents) > settings.max_upload_bytes:
            max_mb = settings.max_upload_bytes // (1024 * 1024)
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum upload size of {max_mb} MB",
            )

        temp_path = None
        transformed_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(contents)
                temp_path = temp_file.name

            transformed_path = excel_transformer.transform_excel(temp_path)
            rag_engine.ingest_data(transformed_path)

            master_path = settings.resolve_master_excel()
            master_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(transformed_path, master_path)
            transformed_path = None

            return {"status": "File transformed and data ingested successfully"}
        except Exception as exc:
            logger.exception("Upload processing failed")
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            if transformed_path and os.path.exists(transformed_path):
                os.remove(transformed_path)

    @app.post("/chat", tags=["ai"])
    @limiter.limit(settings.chat_rate_limit)
    async def chat(request: Request, body: QueryRequest):
        try:
            hist_dicts = [{"role": msg.role, "content": msg.content} for msg in body.history]
            response = rag_engine.handle_query(body.query, hist_dicts)
            return {"response": response}
        except Exception as exc:
            logger.exception("Chat error")
            err_str = str(exc).lower()
            auth_tokens = ("api_key", "api key", "auth", "connection", "rate limit")
            if any(token in err_str for token in auth_tokens):
                friendly_msg = (
                    "Oh no! I lost connection to the AI co-pilot. "
                    "Please verify your OpenAI or Groq API key in environment variables. 🌿"
                )
            else:
                friendly_msg = (
                    f"I encountered an error trying to process your request: {exc}. "
                    "Please check your backend configurations. 🌿"
                )
            return {"response": friendly_msg}

    @app.post("/ingest", tags=["data"])
    async def ingest():
        excel_path = settings.resolve_master_excel()
        if not excel_path.exists():
            raise HTTPException(status_code=404, detail="Master Excel file not found")
        try:
            rag_engine.ingest_data(str(excel_path))
            return {"status": "Data ingested successfully"}
        except Exception as exc:
            logger.exception("Ingest failed")
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    static_path = Path(__file__).parent / "static"
    if static_path.exists():
        app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
