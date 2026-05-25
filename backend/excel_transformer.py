import pandas as pd
import os

def transform_excel(file_path):
    """
    Ensures the uploaded file (Excel or CSV) follows the ELITE HR Master Specification.
    Maps common column variations and creates/populates missing sheets.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    # Required sheets and their key columns
    required_structure = {
        "India Employee Database": ["Employee ID", "Employee Name", "Department"],
        "US Employee Database": ["Employee ID", "Employee Name", "Department"],
        "Productivity": ["Employee ID", "Avg Hrs/Day"],
        "Offboarded Resources": ["Employee ID"],
        "SecOps_Keycloak": ["Employee ID", "Account Status", "MFA Enrolled"],
        "Finance": ["Employee ID", "Annual CTC"]
    }
    
    output_path = f"transformed_{os.path.splitext(os.path.basename(file_path))[0]}.xlsx"
    
    def clean_df(df):
        # Rename common column variations
        col_map = {
            "emp id": "Employee ID",
            "employeeid": "Employee ID",
            "id": "Employee ID",
            "emp_id": "Employee ID",
            "employee id": "Employee ID",
            "name": "Employee Name",
            "emp name": "Employee Name",
            "employeename": "Employee Name",
            "emp_name": "Employee Name",
            "employee name": "Employee Name",
            "dept": "Department",
            "dept_name": "Department",
            "departmentname": "Department",
            "department": "Department",
            "overall avg hrs/day": "Avg Hrs/Day",
            "avg hours": "Avg Hrs/Day",
            "hours": "Avg Hrs/Day",
            "avg hrs/day": "Avg Hrs/Day",
            "avg_hrs_day": "Avg Hrs/Day",
            "status": "Account Status",
            "active": "Account Status",
            "account status": "Account Status",
            "mfa": "MFA Enrolled",
            "mfa_enrolled": "MFA Enrolled",
            "mfa active": "MFA Enrolled",
            "mfa enrolled": "MFA Enrolled",
            "ctc": "Annual CTC",
            "salary": "Annual CTC",
            "annual_ctc": "Annual CTC",
            "annual ctc": "Annual CTC"
        }
        rename_dict = {}
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if col_lower in col_map:
                rename_dict[col] = col_map[col_lower]
        df.rename(columns=rename_dict, inplace=True)
        return df

    if ext == ".csv":
        # Load CSV using pandas
        try:
            df_csv = pd.read_csv(file_path)
        except Exception:
            # Try with different encoding/separator if default fails
            df_csv = pd.read_csv(file_path, encoding="latin1", on_bad_lines="skip")
            
        df_csv = clean_df(df_csv)
        
        # Ensure Employee ID exists
        if "Employee ID" not in df_csv.columns:
            # Generate temporary IDs
            df_csv["Employee ID"] = [f"EMP{str(i).zfill(3)}" for i in range(1, len(df_csv) + 1)]
            
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 1. India and US split based on country column
            country_col = None
            for col in df_csv.columns:
                if str(col).lower().strip() in ["country", "location", "region"]:
                    country_col = col
                    break
                    
            if country_col:
                india_mask = df_csv[country_col].astype(str).str.lower().str.contains("india|in", na=False)
                df_india = df_csv[india_mask].copy()
                df_us = df_csv[~india_mask].copy()
            else:
                df_india = df_csv.copy()
                df_us = pd.DataFrame(columns=["Employee ID", "Employee Name", "Department"])
                
            # Clean and write India Database
            for col in required_structure["India Employee Database"]:
                if col not in df_india.columns:
                    df_india[col] = "N/A"
            df_india[required_structure["India Employee Database"]].to_excel(writer, sheet_name="India Employee Database", index=False)
            
            # Clean and write US Database
            for col in required_structure["US Employee Database"]:
                if col not in df_us.columns:
                    df_us[col] = "N/A"
            df_us[required_structure["US Employee Database"]].to_excel(writer, sheet_name="US Employee Database", index=False)
            
            # 2. Productivity
            df_prod = df_csv.copy()
            if "Avg Hrs/Day" not in df_prod.columns:
                df_prod["Avg Hrs/Day"] = 8.0
            df_prod[required_structure["Productivity"]].to_excel(writer, sheet_name="Productivity", index=False)
            
            # 3. Offboarded Resources
            df_off = pd.DataFrame(columns=["Employee ID"])
            status_col = "Account Status" if "Account Status" in df_csv.columns else None
            if status_col:
                off_mask = df_csv[status_col].astype(str).str.lower().str.contains("inactive|terminated|offboarded", na=False)
                df_off = df_csv[off_mask][["Employee ID"]].copy()
            df_off.to_excel(writer, sheet_name="Offboarded Resources", index=False)
            
            # 4. SecOps_Keycloak
            df_kc = df_csv.copy()
            if "Account Status" not in df_kc.columns:
                df_kc["Account Status"] = "Active"
            if "MFA Enrolled" not in df_kc.columns:
                df_kc["MFA Enrolled"] = "Yes"
            df_kc[required_structure["SecOps_Keycloak"]].to_excel(writer, sheet_name="SecOps_Keycloak", index=False)
            
            # 5. Finance
            df_fin = df_csv.copy()
            if "Annual CTC" not in df_fin.columns:
                df_fin["Annual CTC"] = "N/A"
            df_fin[required_structure["Finance"]].to_excel(writer, sheet_name="Finance", index=False)
            
    else:
        # Load Excel file
        xl = pd.ExcelFile(file_path)
        sheets = xl.sheet_names
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for target_sheet, required_cols in required_structure.items():
                source_sheet = None
                for s in sheets:
                    if target_sheet.lower() in s.lower() or s.lower() in target_sheet.lower():
                        source_sheet = s
                        break
                
                if source_sheet:
                    df = xl.parse(source_sheet)
                    df = clean_df(df)
                    
                    for col in required_cols:
                        if col not in df.columns:
                            df[col] = "N/A"
                    
                    df[required_cols].to_excel(writer, sheet_name=target_sheet, index=False)
                else:
                    df = pd.DataFrame(columns=required_cols)
                    df.to_excel(writer, sheet_name=target_sheet, index=False)
                    
            # Copy any other existing sheets
            for s in sheets:
                if not any(target.lower() in s.lower() for target in required_structure.keys()):
                    xl.parse(s).to_excel(writer, sheet_name=s, index=False)
                    
    return output_path
