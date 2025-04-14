# 챗봇 라우터, 챗봇 서비스(ChatbotService.py)를 사용 
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from AzureServiceModule.ChatbotService import ChatbotService 
import os 
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
chatbot_service = ChatbotService(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    endpoint=os.getenv("ENDPOINT_URL"),
    deployment=os.getenv("DEPLOYMENT_NAME"),
    search_key=os.getenv("SEARCH_KEY"),
    search_endpoint=os.getenv("SEARCH_ENDPOINT"),
    search_index=os.getenv("SEARCH_INDEX_NAME")
)

@router.post("/response")
async def respond(request: Request):
    body = await request.json()
    user_input = body.get("input", "")
    history = body.get("history", [])

    if not user_input:
        return JSONResponse(content={"error": "입력값이 비어 있습니다."}, status_code=400)

    try:
        result = await chatbot_service.handle_user_input(user_input, history)
        return JSONResponse(content=result)
# 프론트엔드에서 접근할 수 있는 형식
# response.data.chat_history
# response.data.structured_data
# response.data.structured_json
# response.data.response_text
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
