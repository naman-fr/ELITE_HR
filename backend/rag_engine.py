import os
import pandas as pd
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Local ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="hr_data")

def serialize_excel(file_path):
    # Load sheets
    xl = pd.ExcelFile(file_path)
    all_chunks = []
    
    for sheet in xl.sheetnames:
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
