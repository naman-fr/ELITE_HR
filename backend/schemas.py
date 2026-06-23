from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    history: list[ChatMessage] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    master_data_available: bool
    llm_provider: str
