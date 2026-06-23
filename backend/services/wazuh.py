"""Wazuh XDR integration with live API and Excel-backed simulation fallback."""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
import requests

from config import Settings, get_settings

logger = logging.getLogger(__name__)

PLACEHOLDER_HOSTS = {"your-wazuh-manager", "company.com", "localhost"}


def _is_configured(settings: Settings) -> bool:
    has_creds = bool(
        settings.wazuh_api_key
        or (settings.wazuh_api_user and settings.wazuh_api_password)
    )
    if not has_creds:
        return False
    url_lower = settings.wazuh_api_url.lower()
    return not any(token in url_lower for token in PLACEHOLDER_HOSTS)


def _authenticate(settings: Settings) -> tuple[str | None, str]:
    if settings.wazuh_api_key:
        return settings.wazuh_api_key, ""

    if not settings.wazuh_api_user or not settings.wazuh_api_password:
        return None, "Wazuh credentials are not configured."

    token_url = f"{settings.wazuh_api_url.rstrip('/')}/security/user/authenticate"
    try:
        response = requests.post(
            token_url,
            auth=(settings.wazuh_api_user, settings.wazuh_api_password),
            verify=False,
            timeout=5,
        )
        if response.status_code != 200:
            return None, f"Authentication failed: HTTP {response.status_code}"
        payload = response.json()
        token = payload.get("data", {}).get("token") or payload.get("token")
        if not token:
            return None, "Authentication response did not include a token."
        return token, ""
    except requests.RequestException as exc:
        logger.warning("Wazuh authentication error: %s", exc)
        return None, f"Connection error: {exc}"


def _fetch_agents(settings: Settings, token: str) -> tuple[list[dict[str, Any]], str]:
    agents_url = f"{settings.wazuh_api_url.rstrip('/')}/agents"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(
            agents_url,
            headers=headers,
            params={"limit": 100, "sort": "-dateAdd"},
            verify=False,
            timeout=5,
        )
        if response.status_code != 200:
            return [], f"Failed to fetch agents: HTTP {response.status_code}"
        items = response.json().get("data", {}).get("affected_items", [])
        agents = []
        for agent in items:
            status = str(agent.get("status", "unknown")).lower()
            risk = "Safe" if status == "active" else "Offline"
            agents.append(
                {
                    "name": agent.get("name", "Unknown Agent"),
                    "device": agent.get("id", "N/A"),
                    "risk": risk,
                    "status": status,
                    "source": "wazuh",
                }
            )
        return agents, ""
    except requests.RequestException as exc:
        logger.warning("Wazuh agents fetch error: %s", exc)
        return [], f"Connection error: {exc}"


def _simulate_from_excel(excel_path) -> list[dict[str, Any]]:
    xl = pd.ExcelFile(excel_path)
    df_india = xl.parse("India Employee Database")
    df_us = xl.parse("US Employee Database")
    df_emp = pd.concat([df_india, df_us], ignore_index=True)

    df_off = (
        xl.parse("Offboarded Resources")
        if "Offboarded Resources" in xl.sheet_names
        else pd.DataFrame()
    )
    df_kc = xl.parse("SecOps_Keycloak") if "SecOps_Keycloak" in xl.sheet_names else pd.DataFrame()

    off_ids = set()
    if not df_off.empty and "Employee ID" in df_off.columns:
        off_ids = {
            str(value).split(".")[0].strip().lower()
            for value in df_off["Employee ID"].dropna().unique()
        }

    mfa_by_id: dict[str, str] = {}
    if not df_kc.empty and "Employee ID" in df_kc.columns:
        for _, row in df_kc.iterrows():
            emp_id = str(row.get("Employee ID", "")).split(".")[0].strip().lower()
            mfa_by_id[emp_id] = str(row.get("MFA Enrolled", "Yes")).strip().lower()

    alerts: list[dict[str, Any]] = []
    for index, row in df_emp.iterrows():
        name = str(row.get("Employee Name", f"Employee {index + 1}"))
        emp_id = str(row.get("Employee ID", "")).split(".")[0].strip().lower()
        region = "IN" if index < len(df_india) else "US"
        device = f"LAPTOP-{region}-{emp_id.upper()}"

        if emp_id in off_ids:
            risk = "Account Orphaned"
        elif mfa_by_id.get(emp_id, "yes") in {"no", "false", "0"}:
            risk = "MFA Warning"
        else:
            risk = "Safe"

        alerts.append(
            {
                "name": name,
                "device": device,
                "risk": risk,
                "status": "simulated",
                "source": "excel",
            }
        )
    return alerts[:50]


def get_wazuh_status(excel_path=None) -> dict[str, Any]:
    settings = get_settings()

    if _is_configured(settings):
        token, error = _authenticate(settings)
        if token:
            agents, fetch_error = _fetch_agents(settings, token)
            if agents:
                safe_count = sum(1 for agent in agents if agent["risk"] == "Safe")
                return {
                    "status": "Connected",
                    "connected": True,
                    "total_agents": len(agents),
                    "safe_agents": safe_count,
                    "alerts": agents[:20],
                }
            error = fetch_error or error

    if excel_path is None:
        excel_path = settings.resolve_master_excel()

    simulated = _simulate_from_excel(excel_path)
    safe_count = sum(1 for item in simulated if item["risk"] == "Safe")
    return {
        "status": "Offline (Simulation Mode)",
        "connected": False,
        "total_agents": len(simulated),
        "safe_agents": safe_count,
        "alerts": simulated,
        "error": "Wazuh is not configured or unreachable. Using Excel-backed simulation.",
    }
