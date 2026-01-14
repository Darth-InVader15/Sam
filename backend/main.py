from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.llm_manager import LLMManager

app = FastAPI(title="SAM API", description="Backend for Context-Aware Offline AI Companion")

# Initialize LLM Manager
llm_manager = LLMManager()

class ChatRequest(BaseModel):
    message: str
    mode: str = "default" # Placeholder for future persona logic

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"status": "SAM Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to generate text response from LLM.
    """
    try:
        # For now, we just pass the message directly.
        # Future: inject system prompt based on request.mode
        response_text = llm_manager.generate_response(request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
