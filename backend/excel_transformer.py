import pandas as pd
import os

def transform_excel(file_path):
    """
    Ensures the Excel file follows the ELITE HR Master Specification.
    Maps common column variations and creates missing sheets.
    """
    xl = pd.ExcelFile(file_path)
    sheets = xl.sheet_names
    
    # Required sheets and their key columns
    required_structure = {
        "India Employee Database": ["Employee ID", "Employee Name", "Department"],
        "US Employee Database": ["Employee ID", "Employee Name", "Department"],
        "Productivity": ["Employee ID", "Avg Hrs/Day"],
        "Offboarded Resources": ["Employee ID"],
        "SecOps_Keycloak": ["Employee ID", "Account Status", "MFA Enrolled"],
        "Finance": ["Employee ID", "Annual CTC"]
    }
    
    output_path = f"transformed_{os.path.basename(file_path)}"
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for target_sheet, required_cols in required_structure.items():
            # Try to find a matching sheet
            source_sheet = None
            for s in sheets:
                if target_sheet.lower() in s.lower() or s.lower() in target_sheet.lower():
                    source_sheet = s
                    break
            
            if source_sheet:
                df = xl.parse(source_sheet)
                # Map column names
                col_map = {
                    "Emp ID": "Employee ID",
                    "ID": "Employee ID",
                    "Name": "Employee Name",
                    "Emp Name": "Employee Name",
                    "Dept": "Department",
                    "Overall Avg Hrs/Day": "Avg Hrs/Day",
                    "Status": "Account Status",
                    "MFA": "MFA Enrolled"
                }
                df.rename(columns=col_map, inplace=True)
                
                # Ensure required columns exist
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = "N/A"
                
                df.to_excel(writer, sheet_name=target_sheet, index=False)
            else:
                # Create empty sheet with headers
                df = pd.DataFrame(columns=required_cols)
                df.to_excel(writer, sheet_name=target_sheet, index=False)
                
        # Copy any other existing sheets
        for s in sheets:
            if not any(target.lower() in s.lower() for target in required_structure.keys()):
                xl.parse(s).to_excel(writer, sheet_name=s, index=False)
                
    return output_path
