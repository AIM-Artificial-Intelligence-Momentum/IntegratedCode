from fastapi import APIRouter, Request
from backend.AzureServiceModule.AzureCLUClient import AzureCLUClient
from backend.AzureServiceModule.backup.AzureOpenAIChat import AzureOpenAIChat

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
        system_prompt = """너는 사용자 의도를 CLU로 분석한 뒤 이에 맞춰 정확하고 풍부한 정보를 제공하는 GPT야.
        사용자는 이런식으로 얘기를 할꺼야.
        공연명: 
        장소: 
        일정:
        유형:
        타겟:
        예상 관객 수:
        예산:
        상태:
    사용자 인텐트는 '{intent}'이고, 엔터티는 {entities}야.
    이를 바탕으로 자연스럽고 정확하게 안내해줘.
    """
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
