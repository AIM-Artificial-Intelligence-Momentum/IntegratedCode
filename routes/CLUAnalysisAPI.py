from fastapi import APIRouter, Request
from backend.AzureServiceModule.AzureCLUClient import AzureCLUClient
from backend.AzureServiceModule.AzureOpenAIChat import AzureOpenAIChat

router = APIRouter()
clu_client = AzureCLUClient()
chat_engine = AzureOpenAIChat()

@router.post("/route")
async def route_by_intent(request: Request):
    body = await request.json()
    user_input = body.get("input", "")

    if not user_input:
        return {"error": "입력값이 비어 있습니다."}

    # 1. CLU로 intent 분석
    clu_result = clu_client.analyze(user_input)
    intent = clu_client.get_top_intent(clu_result)
    entities = clu_client.get_entities(clu_result)

    # 2. Intent 기반 분기 처리
    if intent == "공연_추천":
        system_prompt = "사용자에게 공연을 추천하는 친절한 챗봇입니다. 사용자 요청을 반영해 자연스럽게 공연을 추천하세요."
        response = chat_engine.run_conversation(user_input, [], system_prompt)
        return {"intent": intent, "entities": entities, "response": response}

    elif intent == "공연_정보_질문":
        # [TODO] KOPIS 연동 후 실제 공연 정보 제공
        return {
            "intent": intent,
            "entities": entities,
            "response": "이건 KOPIS API로 공연 정보를 검색해서 응답할 예정입니다."
        }

    elif intent == "공연_예매_문의":
        return {
            "intent": intent,
            "entities": entities,
            "response": "공연 예매 관련 정보는 예매처에서 확인하실 수 있습니다. (추후 연동 예정)"
        }

    else:
        # 기타 → GPT로 자연어 답변
        response = chat_engine.run_conversation(user_input, [])
        return {"intent": intent, "entities": entities, "response": response}
