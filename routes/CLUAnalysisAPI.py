from fastapi import APIRouter, Request
from backend.AzureServiceModule.ServiceRouter import ServiceRouter
from fastapi.responses import JSONResponse

router = APIRouter()
router_service = ServiceRouter()

@router.post("/route")
async def route_by_intent(request: Request):
    body = await request.json()
    user_input = body.get("input", "")
    history = body.get("history", [])

    if not user_input:
        return JSONResponse(content={"error": "입력값이 비어 있습니다."}, status_code=400)

    try:
        result = await router_service.handle_user_input(user_input, history)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
