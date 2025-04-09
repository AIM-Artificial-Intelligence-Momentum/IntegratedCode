# routes/analysis_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np

# analysis_module.py를 import
# (※ 경로 주의: 폴더 구조에 따라 from ..analysis_module import ... 등 사용)
from analysis_module import (
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
    region: str
    start_date_numeric: float
    capacity: float
    star_power: float
    ticket_price: float
    marketing_budget: float
    sns_mention_count: float
    daily_sales: float
    booking_rate: float
    ad_exposure: float
    sns_mention_daily: float

@router.post("/accumulated_sales")
def api_predict_accumulated_sales(inputs: List[AccSalesInput]):
    input_data = [inp.dict() for inp in inputs]
    preds = predict_accumulated_sales(input_data)
    return {"predictions": preds.tolist()}


# ------------------------------------------
# 2) 회귀: 손익 예측 (ROI, BEP)
# ------------------------------------------
class ROI_BEP_Input(BaseModel):
    production_cost: float
    marketing_budget: float
    ticket_price: float
    capacity: float
    variable_cost_rate: float
    accumulated_sales: float

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
    region: str
    start_date_numeric: float
    capacity: float
    star_power: float
    daily_sales: float
    accumulated_sales: float
    ad_exposure: float
    sns_mention_daily: float
    promo_event_flag: int

@router.post("/ticket_risk")
def api_predict_ticket_risk(inputs: List[TicketRiskInput]):
    input_data = [inp.dict() for inp in inputs]
    preds = predict_ticket_risk(input_data)
    return {"risk_labels": preds.tolist()}


# ------------------------------------------
# 4) 군집: 관객 세분화
# ------------------------------------------
class AudienceClusterInput(BaseModel):
    recency_days: float
    booking_count: float
    total_amount: float
    age: float

@router.post("/audience_cluster")
def api_predict_audience_cluster(inputs: List[AudienceClusterInput]):
    input_data = [inp.dict() for inp in inputs]
    clusters = predict_audience_cluster(input_data)
    return {"clusters": clusters.tolist()}
