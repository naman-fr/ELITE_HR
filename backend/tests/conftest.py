import pytest
from fastapi.testclient import TestClient

from config import Settings
from main import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    excel_path = tmp_path / "ELITE_HR_Master_Dashboard.xlsx"
    monkeypatch.setenv("MASTER_EXCEL_PATH", str(excel_path))
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("APP_ENV", "test")

    settings = Settings()
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client, excel_path
