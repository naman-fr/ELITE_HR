"""Application configuration loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ELITE HR Intelligence API"
    app_version: str = "2.1.0"
    environment: str = Field(default="development", alias="APP_ENV")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")

    wazuh_api_url: str = Field(
        default="https://api.cloud.wazuh.com/v2",
        alias="WAZUH_API_URL",
    )
    wazuh_api_user: str | None = Field(default=None, alias="WAZUH_API_USER")
    wazuh_api_password: str | None = Field(default=None, alias="WAZUH_API_PASSWORD")
    wazuh_api_key: str | None = Field(default=None, alias="WAZUH_API_KEY")

    keycloak_url: str | None = Field(default=None, alias="KEYCLOAK_URL")
    keycloak_realm: str = Field(default="master", alias="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(default="hr-platform", alias="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str | None = Field(default=None, alias="KEYCLOAK_CLIENT_SECRET")

    chroma_db_path: Path = Field(default=Path("./chroma_db"))
    master_excel_path: Path | None = Field(default=None, alias="MASTER_EXCEL_PATH")

    max_upload_bytes: int = Field(default=10 * 1024 * 1024, alias="MAX_UPLOAD_BYTES")
    chat_rate_limit: str = Field(default="30/minute", alias="CHAT_RATE_LIMIT")

    @property
    def is_groq(self) -> bool:
        return bool(self.openai_api_key and str(self.openai_api_key).startswith("gsk_"))

    @property
    def llm_base_url(self) -> str | None:
        return "https://api.groq.com/openai/v1" if self.is_groq else None

    @property
    def llm_model(self) -> str:
        return "llama-3.3-70b-versatile" if self.is_groq else "gpt-4o"

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def resolve_master_excel(self) -> Path:
        if self.master_excel_path and self.master_excel_path.exists():
            return self.master_excel_path

        candidates = [
            Path("/ELITE_HR_Master_Dashboard.xlsx"),
            Path("../ELITE_HR_Master_Dashboard.xlsx"),
            Path("ELITE_HR_Master_Dashboard.xlsx"),
            Path(__file__).resolve().parent.parent / "ELITE_HR_Master_Dashboard.xlsx",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[1]


@lru_cache
def get_settings() -> Settings:
    return Settings()
