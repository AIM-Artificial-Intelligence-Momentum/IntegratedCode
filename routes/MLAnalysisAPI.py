# routes/analysis_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np

# analysis_module.py를 import
# (※ 경로 주의: 폴더 구조에 따라 from ..analysis_module import ... 등 사용)
from backend.ModelPredictionModule.analysis_module import (
    predict_accumulated_sales,
    predict_roi_bep,
    predict_ticket_risk,
    predict_audience_cluster
)

router = APIRouter()
# ------------------------------------------
# 1) 회귀: 관객 수 예측
# ------------------------------------------
class AccSalesInput(BaseModel):
    genre: str
    region: str = "서울특별시"
    start_date_numeric: float = 1
    capacity: float = 502000.5
    star_power: float = 280.0
    ticket_price: float = = 40439.5
    marketing_budget: float = 8098512.5
    sns_mention_count: float = 38.0
    daily_sales: float = 2.0
    booking_rate: float = 0.7
    ad_exposure: float = 303284.5
    sns_mention_daily: float = 38.0

@router.post("/accumulated_sales")
def api_predict_accumulated_sales(inputs: List[AccSalesInput]):
    input_data = [inp.dict() for inp in inputs]
    preds = predict_accumulated_sales(input_data)
    return {"predictions": preds.tolist()}


# ------------------------------------------
# 2) 회귀: 손익 예측 (ROI, BEP)
# ------------------------------------------
class ROI_BEP_Input(BaseModel):
    production_cost: float = 570111934.0
    marketing_budget: float = 8098512.5
    ticket_price: float = 40349.5
    capacity: float = 280.0
    variable_cost_rate: float = 0.17754999999999999
    accumulated_sales: float = 105.0

@router.post("/roi_bep")
def api_predict_roi_bep(inputs: List[ROI_BEP_Input]):
    input_data = [inp.dict() for inp in inputs]
    preds = predict_roi_bep(input_data)
    return {"predictions": preds.tolist()}


# ------------------------------------------
# 3) 분류: 티켓 판매 위험 예측
# ------------------------------------------
class TicketRiskInput(BaseModel):
    genre: str
    region: str = "서울특별시"
    start_date_numeric: float = "1"
    capacity: float = "280.0"
    star_power: float = "1" # default : 1
    daily_sales: float = 2.0
    accumulated_sales: float = 105.0
    ad_exposure: float = 303284.5
    sns_mention_daily: float = 0
    promo_event_flag: int = 0.0

@router.post("/ticket_risk")
def api_predict_ticket_risk(inputs: List[TicketRiskInput]):
    input_data = [inp.dict() for inp in inputs]
    preds = predict_ticket_risk(input_data)
    return {"risk_labels": preds.tolist()}


# ------------------------------------------
# 4) 군집: 관객 세분화
# ------------------------------------------
class AudienceClusterInput(BaseModel):
    booking_count: float = 4.0
    total_amount: float = 62675.5
    age: float = 34.0
    recency_days: float = 1

@router.post("/audience_cluster")
def api_predict_audience_cluster(inputs: List[AudienceClusterInput]):
    input_data = [inp.dict() for inp in inputs]
    clusters = predict_audience_cluster(input_data)
    return {"clusters": clusters.tolist()}
