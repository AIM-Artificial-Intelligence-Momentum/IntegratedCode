#ChatbotAPI.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from backend.AzureServiceModule.AzureOpenAIChat import AzureOpenAIChat
router = APIRouter()
chatbot = AzureOpenAIChat()

class ChatRequest(BaseModel):
    prompt: str
    history: list = []

@router.post("/chat")
async def chat_with_body(request: ChatRequest):
    try:
        _, updated_history = chatbot.chatgpt_response(request.prompt, request.history)
        return {"reply": updated_history[-1]["content"], "history": updated_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
