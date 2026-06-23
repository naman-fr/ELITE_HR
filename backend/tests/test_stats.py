import pandas as pd


def _write_master_workbook(path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame(
            {
                "Employee ID": ["IN001", "IN002"],
                "Employee Name": ["Aditya Taylor", "Kiran Verma"],
                "Department": ["Engineering", "Sales"],
            }
        ).to_excel(writer, sheet_name="India Employee Database", index=False)
        pd.DataFrame(
            {
                "Employee ID": ["US001"],
                "Employee Name": ["Priya Harris"],
                "Department": ["Operations"],
            }
        ).to_excel(writer, sheet_name="US Employee Database", index=False)
        pd.DataFrame(
            {
                "Employee ID": ["IN001", "IN002", "US001"],
                "Avg Hrs/Day": [8.5, 7.2, 8.0],
            }
        ).to_excel(writer, sheet_name="Productivity", index=False)
        pd.DataFrame({"Employee ID": ["US001"]}).to_excel(
            writer, sheet_name="Offboarded Resources", index=False
        )
        pd.DataFrame(
            {
                "Employee ID": ["IN001", "IN002", "US001"],
                "Account Status": ["Active", "Active", "Active"],
                "MFA Enrolled": ["Yes", "No", "Yes"],
            }
        ).to_excel(writer, sheet_name="SecOps_Keycloak", index=False)
        pd.DataFrame(
            {
                "Employee ID": ["IN001", "IN002", "US001"],
                "Annual CTC": ["1200000", "900000", "85000"],
            }
        ).to_excel(writer, sheet_name="Finance", index=False)


def test_stats_endpoint_returns_workforce_metrics(client):
    test_client, excel_path = client
    _write_master_workbook(excel_path)

    response = test_client.get("/stats")
    assert response.status_code == 200
    payload = response.json()
    assert payload["headcount"] == 3
    assert payload["avg_productivity"] > 0
    assert isinstance(payload["departments"], list)


def test_wazuh_simulation_mode(client):
    test_client, excel_path = client
    _write_master_workbook(excel_path)

    response = test_client.get("/wazuh/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["connected"] is False
    assert payload["alerts"]
    assert any(alert["risk"] != "Safe" for alert in payload["alerts"])
