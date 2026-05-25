from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import rag_engine
import excel_transformer
import os
import shutil
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ELITE HR Intelligence API")

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    query: str
    history: list[ChatMessage] = []

@app.get("/health")
def read_root():
    return {"status": "ELITE HR API is online"}

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        temp_path = f"raw_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transform the file to standard format
        transformed_path = excel_transformer.transform_excel(temp_path)
        
        # Ingest the transformed data
        rag_engine.ingest_data(transformed_path)
        
        # Move to master location
        shutil.move(transformed_path, "../ELITE_HR_Master_Dashboard.xlsx")
        
        # Cleanup
        os.remove(temp_path)
        
        return {"status": "File transformed and data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        excel_path = "../ELITE_HR_Master_Dashboard.xlsx"
        if not os.path.exists(excel_path):
            excel_path = "ELITE_HR_Master_Dashboard.xlsx"
            if not os.path.exists(excel_path):
                return {"error": "Excel file not found"}
        stats = rag_engine.get_excel_stats(excel_path)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        # Convert request history objects to list of dicts for handle_query
        hist_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]
        response = rag_engine.handle_query(request.query, hist_dicts)
        return {"response": response}
    except Exception as e:
        print(f"Chat error: {e}")
        err_str = str(e).lower()
        if "api_key" in err_str or "api key" in err_str or "auth" in err_str or "connection" in err_str or "rate limit" in err_str:
            friendly_msg = "Oh no! I lost connection to the AI co-pilot. Please make sure that your OpenAI or Groq API key is correctly configured in your Hugging Face Space secrets or environment variables. 🌿"
        else:
            friendly_msg = f"I encountered an error trying to process your request: {str(e)}. Please check your backend configurations. 🌿"
        return {"response": friendly_msg}

@app.post("/ingest")
async def ingest():
    try:
        excel_path = "../ELITE_HR_Master_Dashboard.xlsx"
        if not os.path.exists(excel_path):
            excel_path = "ELITE_HR_Master_Dashboard.xlsx"
            if not os.path.exists(excel_path):
                return {"error": "Excel file not found"}
        rag_engine.ingest_data(excel_path)
        return {"status": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.staticfiles import StaticFiles

# Serve frontend static assets if available
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
