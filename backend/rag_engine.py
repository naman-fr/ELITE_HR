import os
import pandas as pd
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    
    # Construct prompt
    system_prompt = "You are an elite HR Intelligence Assistant. Use the provided context to answer precisely. Cite sources like [India DB]."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context: {' '.join(context)}\n\nQuery: {query}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )
    
    return response.choices[0].message.content

def get_excel_stats(file_path):
    xl = pd.ExcelFile(file_path)
    df_india = xl.parse("India Employee Database")
    df_us = xl.parse("US Employee Database")
    df_prod = xl.parse("Productivity")
    
    total_headcount = len(df_india) + len(df_us)
    avg_prod = df_prod["Avg Hrs/Day"].mean()
    
    # Mock some others based on data if available, else defaults
    dept_counts = pd.concat([df_india["Department"], df_us["Department"]]).value_counts().to_dict()
    
    return {
        "headcount": total_headcount,
        "avg_productivity": round(float(avg_prod), 1),
        "compliance_risks": 8, # Placeholder or calc from Risk tab
        "identity_health": 96, # Placeholder or calc from Keycloak tab
        "departments": [{"label": k, "val": int(v)} for k, v in dept_counts.items()]
    }
