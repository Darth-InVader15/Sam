from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.llm_manager import LLMManager

from datetime import datetime
from backend.prompts import PERSONAS
from backend import database

app = FastAPI(title="SAM API", description="Backend for Context-Aware Offline AI Companion")

# Initialize LLM Manager
llm_manager = LLMManager()

class ChatRequest(BaseModel):
    message: str
    mode: str = "default"

class ChatResponse(BaseModel):
    response: str
    mode: str

@app.get("/")
async def root():
    return {"status": "SAM Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to generate text response from LLM with context and persona.
    """
    try:
        # Determine mode and system prompt
        mode = request.mode if request.mode in PERSONAS else "default"
        system_prompt = PERSONAS.get(mode)
        
        # Get history
        history = database.get_recent_history(mode)
        
        # Generate response
        response_text = llm_manager.generate_response(
            prompt=request.message,
            system_prompt=system_prompt,
            history=history
        )
        
        # Save interaction
        database.save_interaction(mode, request.message, response_text)
        
        return ChatResponse(response=response_text, mode=mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
