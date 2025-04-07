from fastapi import APIRouter, UploadFile
from backend.AzureServiceModule.AzureOpenAIChat import AzureOpenAIChat

router = APIRouter()
chatbot = AzureOpenAIChat()

@router.post("/chat")
def chat_with(text: str):
    return chatbot.chatgpt_response()
