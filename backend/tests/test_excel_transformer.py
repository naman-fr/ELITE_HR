import os

import pandas as pd

import excel_transformer


def test_transform_csv_creates_master_workbook(tmp_path):
    csv_path = tmp_path / "employees.csv"
    pd.DataFrame(
        {
            "Employee ID": ["E001", "E002"],
            "Employee Name": ["Jane Doe", "John Smith"],
            "Department": ["Engineering", "HR"],
            "Country": ["India", "United States"],
            "Avg Hrs/Day": [8.1, 7.9],
        }
    ).to_csv(csv_path, index=False)

    output_path = excel_transformer.transform_excel(str(csv_path))
    assert os.path.exists(output_path)

    workbook = pd.ExcelFile(output_path)
    assert "India Employee Database" in workbook.sheet_names
    assert "US Employee Database" in workbook.sheet_names
    assert "Productivity" in workbook.sheet_names

    india = workbook.parse("India Employee Database")
    us = workbook.parse("US Employee Database")
    assert len(india) == 1
    assert len(us) == 1
