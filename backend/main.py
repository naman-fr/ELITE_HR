from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import rag_engine
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

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "ELITE HR API is online"}

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Ingest the uploaded file
        rag_engine.ingest_data(temp_path)
        
        # Move to master location for consistency
        shutil.move(temp_path, "../ELITE_HR_Master_Dashboard.xlsx")
        
        return {"status": "File uploaded and data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        excel_path = "../ELITE_HR_Master_Dashboard.xlsx"
        if not os.path.exists(excel_path):
            return {"error": "Excel file not found"}
        stats = rag_engine.get_excel_stats(excel_path)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        response = rag_engine.handle_query(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest():
    try:
        excel_path = "../ELITE_HR_Master_Dashboard.xlsx"
        if not os.path.exists(excel_path):
            return {"error": "Excel file not found"}
        rag_engine.ingest_data(excel_path)
        return {"status": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
