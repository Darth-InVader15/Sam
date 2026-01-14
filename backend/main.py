from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.llm_manager import LLMManager
from datetime import datetime
from backend.prompts import PERSONAS
from backend import database
from backend.audio_engine import AudioEngine

app = FastAPI(title="SAM API", description="Backend for Context-Aware Offline AI Companion")

# Initialize LLM Manager and Audio Engine
llm_manager = LLMManager()
audio_engine = AudioEngine()

class ChatRequest(BaseModel):
    message: str
    mode: str = "default"

class ChatResponse(BaseModel):
    response: str
    mode: str
    audio_base64: str = ""

@app.get("/")
async def root():
    return {"status": "SAM Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to generate text response from LLM with context and persona, plus audio.
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
        
        # Generate Audio
        audio_b64 = audio_engine.generate_audio(response_text, mode)
        
        return ChatResponse(response=response_text, mode=mode, audio_base64=audio_b64)
    except Exception as e:
        # Log error but return what we can
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
