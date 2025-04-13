# backend/AzureServiceModule/AISearchAPI.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from AzureServiceModule.AzureAISearch import ServiceRouter

router = APIRouter()
router_service = ServiceRouter()

@router.post("/route")
async def azure_ai_search(request: Request):
    body = await request.json()
    user_input = body.get("input", "")
    history = body.get("history", [])

    if not user_input:
        return JSONResponse(content={"error": "입력값이 비어 있습니다."}, status_code=400)

    try:
        result = await router_service.handle_user_input(user_input, history)
        # print(result)
        # {'history': [{'role': 'user', 'content': '티켓 가격이 3만원이고 예상 관객 수가 2000명일 때 총 수익은 얼마일까요? 추가 수익  요소도 고려해 주세요'}, 
        #              {'role': 'assistant', 'content': '티켓 가격이 3만원이고 예상 관객 수가 2000명이라면, 총 수익은 다음 과 같이 계산됩니다:\n\n**기본 티켓 수익:**  \n3만원 × 2000명 = **60,000,000원**\n\n추가 수익 요소를 고려하려면, 다음과 같은 항목을 추가적으로 확인해야 합니다:  \n- 굿즈 판매  \n- 스폰서십  \n- 푸드 및 음료 판매  \n- VIP 패키지  \n\n각 항목에 대한  예상 수익을 알려주시면 더 정확한 총 수익을 계산할 수 있습니다. 추가 정보를 공유해 주시겠습니까?  \n\n현재 JSON 데이터:\n```json\n\n```'}], 
        # 'structured_data': {'show_name': '', 'show_period': '', 'location': '', 'target_audience': 2000, 'predicted_revenue': '60,000,000원', 'estimated_cost': '', 'performers': '', 'marketing_breakdown': [{'category': '', 'value': 0}], 'audience_trend': [2000]}}
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
