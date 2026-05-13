from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import rag_engine
import os
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
