import os
import pandas as pd
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import json
import re

load_dotenv()

# Groq/OpenAI Config
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1" if str(API_KEY).startswith("gsk_") else None

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
DEFAULT_MODEL = "llama-3.3-70b-versatile" if BASE_URL else "gpt-4o"

# Wazuh Cloud Config
WAZUH_API_KEY = os.getenv("WAZUH_API_KEY")
WAZUH_URL = os.getenv("WAZUH_API_URL", "https://api.cloud.wazuh.com/v2")

# Local ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="hr_data")

def serialize_excel(file_path):
    # Load sheets
    xl = pd.ExcelFile(file_path)
    all_chunks = []
    
    for sheet in xl.sheet_names:
        if sheet in ["India Employee Database", "US Employee Database"]:
            df = xl.parse(sheet)
            for _, row in df.iterrows():
                chunk = f"SHEET: {sheet}\n"
                for col in df.columns:
                    chunk += f"{col}: {row[col]}\n"
                all_chunks.append({
                    "id": str(row.get("Employee ID", "unknown")),
                    "text": chunk,
                    "metadata": {"sheet": sheet, "emp_id": str(row.get("Employee ID", ""))}
                })
    return all_chunks

def ingest_data(file_path):
    chunks = serialize_excel(file_path)
    
    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    
    # Simple embedding using OpenAI
    # (In production, use a more efficient way to embed in batches)
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Ingested {len(chunks)} records into vector store.")

def query_rag(query_text):
    results = collection.query(
        query_texts=[query_text],
        n_results=5
    )
    return results["documents"][0]

# Function calling tool definitions (subset)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_employee_profile",
            "description": "Retrieve complete employee record from the databases",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {"type": "string"}
                },
                "required": ["employee_id"]
            }
        }
    }
]

def analyze_dialogue_state(query, history):
    formatted_history = []
    for msg in history:
        role = msg.get("role", "user")
        if role == "ai":
            role = "assistant"
        formatted_history.append({"role": role, "content": msg.get("content", "")})
    
    formatted_history.append({"role": "user", "content": query})
    
    system_prompt = """
You are the Dialogue State Tracking (DST) module of a Task-Oriented Dialogue (TOD) HR-Agent.
Analyze the user's latest query along with the conversation history to perform:
1. Intent Selection: Classify the user's current request into one of these intents:
   - "get_profile": Retrieve details/profile of a specific employee.
   - "check_security": Retrieve security anomalies, XDR/device status of a specific employee or general.
   - "check_mfa": Check MFA enrollment or identity status of a specific employee or general.
   - "productivity_check": Check average productivity hours for employee(s) or department.
   - "attrition_check": Check attrition rates or trends.
   - "general": General conversation or query not fitting the above.
2. Entity Extraction: Extract any entity values mentioned in the query or conversation history:
   - "employee_name": Name of the employee.
   - "employee_id": Employee ID.
   - "department": Name of the department.

Output a valid JSON block ONLY, matching this schema:
{
  "intent": "get_profile" | "check_security" | "check_mfa" | "productivity_check" | "attrition_check" | "general",
  "entities": {
    "employee_name": string | null,
    "employee_id": string | null,
    "department": string | null
  }
}
"""
    
    messages = [
        {"role": "system", "content": system_prompt}
    ] + formatted_history
    
    model = DEFAULT_MODEL
    
    try:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"}
            )
        except Exception:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
        
        content = response.choices[0].message.content
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return json.loads(content)
    except Exception as e:
        print("DST LLM parsing failed, using fallback:", str(e))
        return {
            "intent": "general",
            "entities": {
                "employee_name": None,
                "employee_id": None,
                "department": None
            }
        }

def find_employee_data_locally(excel_path, name=None, emp_id=None):
    if not os.path.exists(excel_path):
        return None
    xl = pd.ExcelFile(excel_path)
    
    df_india = xl.parse("India Employee Database")
    df_us = xl.parse("US Employee Database")
    
    df_india["Database"] = "India Employee Database"
    df_us["Database"] = "US Employee Database"
    df_emp = pd.concat([df_india, df_us], ignore_index=True)
    
    target_row = None
    if emp_id:
        match = df_emp[df_emp["Employee ID"].astype(str).str.strip().str.lower() == str(emp_id).strip().lower()]
        if not match.empty:
            target_row = match.iloc[0]
    elif name:
        match = df_emp[df_emp["Employee Name"].astype(str).str.lower().str.contains(name.lower().strip(), na=False)]
        if not match.empty:
            target_row = match.iloc[0]
            
    if target_row is None:
        return None
        
    emp_details = target_row.to_dict()
    eid = emp_details.get("Employee ID")
    
    if "Productivity" in xl.sheet_names:
        df_prod = xl.parse("Productivity")
        prod_match = df_prod[df_prod["Employee ID"].astype(str).str.strip().str.lower() == str(eid).strip().lower()]
        if not prod_match.empty:
            # Drop Employee ID and Employee Name from prod before update to avoid conflict
            prod_dict = prod_match.iloc[0].to_dict()
            prod_dict.pop("Employee Name", None)
            emp_details.update(prod_dict)
            
    if "Finance" in xl.sheet_names:
        df_fin = xl.parse("Finance")
        fin_match = df_fin[df_fin["Employee ID"].astype(str).str.strip().str.lower() == str(eid).strip().lower()]
        if not fin_match.empty:
            fin_dict = fin_match.iloc[0].to_dict()
            fin_dict.pop("Employee Name", None)
            emp_details.update(fin_dict)
            
    if "SecOps_Keycloak" in xl.sheet_names:
        df_kc = xl.parse("SecOps_Keycloak")
        kc_match = df_kc[df_kc["Employee ID"].astype(str).str.strip().str.lower() == str(eid).strip().lower()]
        if not kc_match.empty:
            kc_dict = kc_match.iloc[0].to_dict()
            kc_dict.pop("Employee Name", None)
            emp_details.update(kc_dict)
            
    if "Offboarded Resources" in xl.sheet_names:
        df_off = xl.parse("Offboarded Resources")
        off_match = df_off[df_off["Employee ID"].astype(str).str.strip().str.lower() == str(eid).strip().lower()]
        emp_details["Offboarded"] = not off_match.empty
        
    return emp_details

def generate_profile_response(emp_data):
    prompt = f"""
You are the Response Generation module of the HR-Agent.
Synthesize a premium employee profile summary based on the following retrieved record:
{emp_data}

Rules:
- Cite the sources properly: use [India DB] or [US DB] for profile details, [Finance] for CTC, [Productivity] for average daily hours.
- Format numbers with units (e.g. ₹ or $ for CTC, "8.2 hrs/day" for productivity).
- Make sure to indicate their Security/MFA status if available.
- Maintain a highly professional, boardroom-ready tone.
"""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_employee_security_response(emp_data):
    prompt = f"""
You are the Response Generation module of the HR-Agent.
Synthesize a security compliance report for this employee based on their retrieved record:
{emp_data}

Rules:
- Cite [Wazuh] for endpoint security/risks, [Keycloak] for account and MFA status.
- Highlight any compliance flags:
  - If offboarded but account status is 'Active' in Keycloak, flag as CRITICAL orphaned account.
  - If MFA is 'No', flag as WARNING MFA Gap.
  - Otherwise mark as Safe / compliant.
- Recommend specific HR action if there are compliance risks.
- Maintain a highly professional, security-aware tone.
"""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_employee_mfa_response(emp_data):
    prompt = f"""
You are the Response Generation module of the HR-Agent.
Summarize the Identity & MFA status of this employee:
{emp_data}

Rules:
- Cite [Keycloak] for account and MFA status.
- State whether they are MFA enrolled and if their account is active.
- Keep it professional and short.
"""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_general_security_response(excel_path):
    if not os.path.exists(excel_path):
        return "I couldn't locate the HR Master Database to check security stats. 🌿"
    xl = pd.ExcelFile(excel_path)
    orphans, mfa_gap = calculate_compliance_metrics(xl)
    
    prompt = f"""
You are the Response Generation module of the HR-Agent.
Summarize the system-wide security compliance status based on the following stats:
- Total Compliance Risks Detected: {orphans + mfa_gap}
- Orphaned Accounts (Offboarded but active in Keycloak): {orphans}
- MFA Gaps (Keycloak users with MFA disabled): {mfa_gap}

Rules:
- Cite [Wazuh] for endpoint risks and [Keycloak] for account/MFA compliance.
- Escalate severity if risks exist: INFO (0 risks) -> WARNING (>0 risks) -> CRITICAL (orphans > 0).
- Recommend specific HR corrective actions (e.g. revoke orphaned logins, enforce MFA policies).
- Maintain a boardroom-ready, professional tone.
"""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_general_mfa_response(excel_path):
    if not os.path.exists(excel_path):
        return "I couldn't locate the HR Master Database to check identity stats. 🌿"
    xl = pd.ExcelFile(excel_path)
    orphans, mfa_gap = calculate_compliance_metrics(xl)
    
    prompt = f"""
You are the Response Generation module of the HR-Agent.
Summarize the Identity & Access Management (IAM) health based on these stats:
- MFA Gaps: {mfa_gap}
- Active Orphans: {orphans}

Rules:
- Cite [Keycloak] for logins, MFA status, and orphaned credentials.
- Outline the importance of MFA compliance and the risk of pending revocations.
- Keep it concise and professional.
"""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_productivity_response(excel_path, emp_name=None, emp_id=None, dept=None):
    if not os.path.exists(excel_path):
        return "I couldn't locate the HR Master Database to check productivity stats. 🌿"
        
    xl = pd.ExcelFile(excel_path)
    df_prod = xl.parse("Productivity")
    
    if emp_name or emp_id:
        emp_data = find_employee_data_locally(excel_path, name=emp_name, emp_id=emp_id)
        if not emp_data:
            searched = emp_id if emp_id else emp_name
            return f"I couldn't find an employee matching '{searched}' to check productivity. 🌿"
        
        avg_hrs = emp_data.get("Avg Hrs/Day", emp_data.get("Overall Avg Hrs/Day", "N/A"))
        prompt = f"""
You are the Response Generation module of the HR-Agent.
Synthesize a productivity report for {emp_data.get('Employee Name')} (ID: {emp_data.get('Employee ID')}):
- Avg Hours/Day: {avg_hrs}
- Department: {emp_data.get('Department')}

Rules:
- Cite [Productivity] as the source.
- Express numbers with units (e.g. "8.2 hrs/day").
- Comment on whether they meet standard workload requirements (typical standard is 8.0 hrs/day).
"""
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
        
    if dept:
        df_india = xl.parse("India Employee Database")
        df_us = xl.parse("US Employee Database")
        df_emp = pd.concat([df_india, df_us], ignore_index=True)
        
        dept_emps = df_emp[df_emp["Department"].astype(str).str.lower() == dept.lower().strip()]
        if dept_emps.empty:
            return f"I couldn't find any records for department '{dept}' in the employee database. 🌿"
            
        dept_ids = dept_emps["Employee ID"].unique()
        dept_prod = df_prod[df_prod["Employee ID"].isin(dept_ids)]
        
        prod_col = "Overall Avg Hrs/Day" if "Overall Avg Hrs/Day" in df_prod.columns else "Avg Hrs/Day"
        avg_hrs = dept_prod[prod_col].mean() if not dept_prod.empty else 8.0
        
        prompt = f"""
You are the Response Generation module of the HR-Agent.
Synthesize a department-level productivity report for the '{dept}' department:
- Average Productivity Hours/Day: {avg_hrs:.1f}
- Number of Employees: {len(dept_prod)}

Rules:
- Cite [Productivity] as the source.
- Express numbers with units.
- Maintain a boardroom-ready tone.
"""
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
        
    prod_col = "Overall Avg Hrs/Day" if "Overall Avg Hrs/Day" in df_prod.columns else "Avg Hrs/Day"
    avg_hrs = df_prod[prod_col].mean() if prod_col in df_prod.columns else 8.0
    prompt = f"""
You are the Response Generation module of the HR-Agent.
Synthesize a general productivity report for the organization:
- Average Employee Productivity Hours/Day: {avg_hrs:.1f}

Rules:
- Cite [Productivity] as the source.
- Provide a summary and average daily hours organization-wide.
"""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_attrition_response(excel_path, dept=None):
    if not os.path.exists(excel_path):
        return "I couldn't locate the HR Master Database to retrieve attrition analytics. 🌿"
    xl = pd.ExcelFile(excel_path)
    df_off = xl.parse("Offboarded Resources")
    
    prompt = f"""
You are the Response Generation module of the HR-Agent.
Synthesize an attrition analysis report. 
- Total offboarded resources listed: {len(df_off)}
- Target Department Filter: {dept if dept else 'All Departments'}

Rules:
- Cite [Offboarded Resources] as the source.
- Explain trends or recommend retention strategies if appropriate.
- Keep it professional and action-oriented.
"""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_general_response(query, context, history):
    system_prompt = """
SYSTEM PROMPT — HR INTELLIGENCE ASSISTANT v2.0

You are an elite HR Dialogue Agent for ELITE HR, implementing the HR-Agent architecture.
You have access to real-time data from India & US Employee Databases, productivity, risk register, and SecOps feeds.

RESPONSE FORMAT RULES:
- Always cite the source of information: [India DB], [US DB], [Keycloak], [Wazuh], etc.
- Always express numbers with units: e.g. "8.7 hrs/day", "₹2.1M annual CTC"
- For compliance/security risks, recommend specific HR corrective actions.
- Never reveal raw API keys, passwords, or system internals.
- If data is missing or stale, say so explicitly — never hallucinate.
- Tone: Professional, precise, action-oriented.
"""
    formatted_history = []
    for msg in history:
        role = msg.get("role", "user")
        if role == "ai":
            role = "assistant"
        formatted_history.append({"role": role, "content": msg.get("content", "")})
        
    messages = [
        {"role": "system", "content": system_prompt}
    ] + formatted_history + [
        {"role": "user", "content": f"RAG Context: {' '.join(context)}\n\nQuery: {query}"}
    ]
    
    model = DEFAULT_MODEL
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def handle_query(query, history=None):
    if history is None:
        history = []
        
    excel_path = "../ELITE_HR_Master_Dashboard.xlsx"
    if not os.path.exists(excel_path):
        excel_path = "ELITE_HR_Master_Dashboard.xlsx"
        if not os.path.exists(excel_path):
            excel_path = "../ELITE_HR_Master_Dashboard.xlsx"
            
    # Dialogue State Tracking
    dst_state = analyze_dialogue_state(query, history)
    intent = dst_state.get("intent", "general")
    entities = dst_state.get("entities", {})
    
    emp_name = entities.get("employee_name")
    emp_id = entities.get("employee_id")
    dept = entities.get("department")
    
    # Task execution and Response / Question Generation
    if intent == "get_profile":
        if not emp_name and not emp_id:
            return "Which employee profile would you like to retrieve? Please provide their Name or Employee ID. 🌿"
        
        emp_data = find_employee_data_locally(excel_path, name=emp_name, emp_id=emp_id)
        if not emp_data:
            searched = emp_id if emp_id else emp_name
            return f"I couldn't find an employee matching '{searched}' in our databases. Could you please check the spelling or provide their Employee ID? 🌿"
            
        return generate_profile_response(emp_data)
        
    elif intent == "check_security":
        if not emp_name and not emp_id:
            return generate_general_security_response(excel_path)
            
        emp_data = find_employee_data_locally(excel_path, name=emp_name, emp_id=emp_id)
        if not emp_data:
            searched = emp_id if emp_id else emp_name
            return f"I couldn't find an employee matching '{searched}' to check their security compliance. Could you please verify the name or ID? 🌿"
            
        return generate_employee_security_response(emp_data)
        
    elif intent == "check_mfa":
        if not emp_name and not emp_id:
            return generate_general_mfa_response(excel_path)
            
        emp_data = find_employee_data_locally(excel_path, name=emp_name, emp_id=emp_id)
        if not emp_data:
            searched = emp_id if emp_id else emp_name
            return f"I couldn't find an employee matching '{searched}' to check their MFA status. Could you please verify the name or ID? 🌿"
            
        return generate_employee_mfa_response(emp_data)
        
    elif intent == "productivity_check":
        return generate_productivity_response(excel_path, emp_name=emp_name, emp_id=emp_id, dept=dept)
        
    elif intent == "attrition_check":
        return generate_attrition_response(excel_path, dept=dept)
        
    else:
        context = query_rag(query)
        return generate_general_response(query, context, history)

def get_keycloak_data():
    """
    Attempts to connect to Keycloak and retrieve real user statistics.
    Returns (connected: bool, users: list, error: str)
    """
    import requests
    keycloak_url = os.getenv("KEYCLOAK_URL")
    realm = os.getenv("KEYCLOAK_REALM", "master")
    client_id = os.getenv("KEYCLOAK_CLIENT_ID", "hr-platform")
    client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
    
    if not keycloak_url or "company.com" in keycloak_url or not client_secret or "your_keycloak_secret" in client_secret:
        return False, [], "Keycloak is not configured or using default placeholders."
        
    try:
        # 1. Get access token via client credentials grant
        token_url = f"{keycloak_url.rstrip('/')}/realms/{realm}/protocol/openid-connect/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        res = requests.post(token_url, data=data, timeout=3)
        if res.status_code != 200:
            return False, [], f"Authentication failed: HTTP {res.status_code}"
            
        token = res.json().get("access_token")
        
        # 2. Get users in the realm
        users_url = f"{keycloak_url.rstrip('/')}/admin/realms/{realm}/users"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        res_users = requests.get(users_url, headers=headers, params={"max": 100}, timeout=3)
        if res_users.status_code != 200:
            return False, [], f"Failed to fetch users: HTTP {res_users.status_code}"
            
        users_data = res_users.json()
        
        processed_users = []
        for u in users_data:
            totp_enabled = u.get("totp", False)
            processed_users.append({
                "username": u.get("username"),
                "email": u.get("email"),
                "enabled": u.get("enabled", True),
                "totp": totp_enabled
            })
            
        return True, processed_users, ""
    except Exception as e:
        return False, [], f"Connection error: {str(e)}"

def calculate_compliance_metrics(xl):
    try:
        connected, kc_users, _ = get_keycloak_data()
        df_off = xl.parse("Offboarded Resources")
        df_jc = xl.parse("SecOps_Keycloak")
        
        off_ids = []
        if "Employee ID" in df_off.columns:
            off_ids = [str(x).split('.')[0].strip().lower() for x in df_off["Employee ID"].dropna().unique()]
            
        orphans = 0
        mfa_gap = 0
        
        if connected and kc_users:
            df_india = xl.parse("India Employee Database")
            df_us = xl.parse("US Employee Database")
            df_emp = pd.concat([df_india, df_us], ignore_index=True)
            
            email_to_id = {}
            name_to_id = {}
            for _, row in df_emp.iterrows():
                eid = str(row.get("Employee ID")).split('.')[0].strip().lower()
                name = str(row.get("Employee Name", "")).strip().lower()
                email = str(row.get("Email", "")).strip().lower()
                if email:
                    email_to_id[email] = eid
                if name:
                    name_to_id[name] = eid
                    
            for u in kc_users:
                u_email = str(u.get("email", "")).strip().lower()
                u_name = str(u.get("username", "")).strip().lower()
                
                emp_id = email_to_id.get(u_email) or name_to_id.get(u_name)
                
                if emp_id:
                    if emp_id in off_ids and u.get("enabled", True):
                        orphans += 1
                    if not u.get("totp", False):
                        mfa_gap += 1
                else:
                    if not u.get("totp", False):
                        mfa_gap += 1
        else:
            if "Employee ID" in df_off.columns and "Employee ID" in df_jc.columns:
                active_jc = [str(x).split('.')[0].strip().lower() for x in df_jc[df_jc["Account Status"].astype(str).str.strip().str.lower() == "active"]["Employee ID"].dropna().unique()]
                orphans = len(set(off_ids).intersection(set(active_jc)))
                
            if "MFA Enrolled" in df_jc.columns:
                mfa_gap = len(df_jc[df_jc["MFA Enrolled"].astype(str).str.strip().str.lower() == "no"])
                
        return orphans, mfa_gap
    except Exception as e:
        print("Error calculating compliance metrics:", e)
        return 0, 0


def get_excel_stats(file_path):
    xl = pd.ExcelFile(file_path)
    df_india = xl.parse("India Employee Database")
    df_us = xl.parse("US Employee Database")
    df_prod = xl.parse("Productivity")
    
    total_headcount = len(df_india) + len(df_us)
    
    # Robust column detection for productivity
    prod_col = "Overall Avg Hrs/Day" if "Overall Avg Hrs/Day" in df_prod.columns else "Avg Hrs/Day"
    avg_prod = df_prod[prod_col].mean() if prod_col in df_prod.columns else 8.0
    
    # Handle NaN in productivity
    import math
    if pd.isna(avg_prod) or math.isnan(avg_prod) or math.isinf(avg_prod):
        avg_prod = 8.0
        
    # Compliance metrics
    orphans, mfa_gap = calculate_compliance_metrics(xl)
    
    # Calculate real department distribution
    dept_counts = pd.concat([df_india["Department"], df_us["Department"]]).value_counts().to_dict()
    
    return {
        "headcount": total_headcount,
        "avg_productivity": round(float(avg_prod), 1),
        "compliance_risks": orphans + mfa_gap,
        "identity_health": int(100 - mfa_gap if total_headcount > 0 else 100),
        "departments": [{"label": str(k), "val": int(v)} for k, v in dept_counts.items() if pd.notna(k)]
    }

