from fastapi import APIRouter
from backend.KopisAPIModule.KopisAPI import KopisAPI

router = APIRouter()
kopis_api = KopisAPI()

@router.get("/performance-list")
def get_performance_list():
    headers, data = kopis_api.fetch_performance_list()
    return {"headers": headers, "data": data}

@router.get("/posters")
def get_posters():
    return kopis_api.fetch_posters_only()
