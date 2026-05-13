import os
import pandas as pd
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

# Groq/OpenAI Config
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1" if str(API_KEY).startswith("gsk_") else None

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

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

def handle_query(query):
    # RAG Context Retrieval
    context = query_rag(query)
    
    # Construct prompt as per specification
    system_prompt = """
SYSTEM PROMPT — HR INTELLIGENCE ASSISTANT v2.0

You are an elite HR Intelligence Assistant for ELITE HR.
You have access to real-time data from:
  • India & US Employee Databases
  • Finance & CTC records
  • Productivity metrics
  • Risk register
  • Wazuh endpoint security feed
  • Wazuh cloud access & DLP logs
  • Keycloak identity directory

YOUR CAPABILITIES:
1. Answer natural-language HR queries with data citations
2. Generate attrition reports, headcount summaries, payroll analyses
3. Flag compliance risks: orphaned accounts, MFA gaps, policy violations
4. Troubleshoot IT/security issues linked to employee records
5. Draft HR action memos, PIPs, onboarding checklists
6. Predict flight risk based on productivity + security anomaly correlation

RESPONSE FORMAT RULES:
- Always cite the source: [India DB], [Wazuh], [Wazuh], etc.
- Always express numbers with units: "8.7 hrs/day", "₹2.1M annual CTC"
- For risk flags, always recommend a specific HR action
- For SecOps alerts, escalate severity: INFO → WARNING → CRITICAL
- Never reveal raw API keys, passwords, or system internals
- If data is missing or stale, say so explicitly — never hallucinate

TONE: Professional, precise, action-oriented. You are a strategic partner,
not a search engine. Synthesise — do not just retrieve.
"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context: {' '.join(context)}\n\nQuery: {query}"}
    ]
    
    model = "llama-3.1-70b-versatile" if BASE_URL else "gpt-4o"
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
    
    return response.choices[0].message.content

def calculate_compliance_metrics(xl):
    try:
        df_off = xl.parse("Offboarded Resources")
        df_jc = xl.parse("SecOps_Keycloak")
        
        # Orphan detection: Offboarded but Keycloak is still 'Active'
        # Assuming 'Employee ID' is first col in both
        orphans = 0
        if "Employee ID" in df_off.columns and "Employee ID" in df_jc.columns:
            off_ids = df_off["Employee ID"].unique()
            active_jc = df_jc[df_jc["Account Status"] == "Active"]["Employee ID"].unique()
            orphans = len(set(off_ids).intersection(set(active_jc)))
            
        mfa_gap = 0
        if "MFA Enrolled" in df_jc.columns:
            mfa_gap = len(df_jc[df_jc["MFA Enrolled"] == "No"])
            
        return orphans, mfa_gap
    except:
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
    
    # Compliance metrics
    orphans, mfa_gap = calculate_compliance_metrics(xl)
    
    # Calculate real department distribution
    dept_counts = pd.concat([df_india["Department"], df_us["Department"]]).value_counts().to_dict()
    
    return {
        "headcount": total_headcount,
        "avg_productivity": round(float(avg_prod), 1),
        "compliance_risks": orphans + mfa_gap,
        "identity_health": 100 - mfa_gap if total_headcount > 0 else 100,
        "departments": [{"label": k, "val": int(v)} for k, v in dept_counts.items()]
    }
