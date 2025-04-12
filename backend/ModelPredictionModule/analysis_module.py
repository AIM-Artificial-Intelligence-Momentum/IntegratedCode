# analysis_module.py

import os
import joblib
import pandas as pd
import numpy as np
from typing import List

FILE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(FILE_DIR, "models")

def load_model(model_name: str):
    """
    model_name: 예) 'xgb_reg_accumulated_sales_planning' (확장자 제외)
    models 폴더에서 해당 pkl 파일을 로드합니다.
    """
    model_path = os.path.join(MODEL_DIR, f"{model_name}.pkl")
    model = joblib.load(model_path)
    return model

# 1) 회귀: 관객 수 예측 - 기획 단계
def predict_acc_sales_planning(input_data: List[dict]) -> dict:
    """
    모델 파일: xgb_reg_accumulated_sales_planning.pkl
    - 기획 단계에서는 유사 공연 비교 데이터와 날짜별 누적 관객 추이(신뢰구간 포함) 등
      가상 데이터를 함께 반환합니다.
    """
    model = load_model("xgb_reg_accumulated_sales_planning")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    
    # 가상 비교 데이터 (5개 공연)
    comparison_data = [
        {"performance_id": 101, "performance_name": "뮤지컬 캣츠", "actual": 2800, "predicted": float(preds[0])},
        {"performance_id": 102, "performance_name": "콘서트 아이유", "actual": 3000, "predicted": float(preds[0]) + 120},
        {"performance_id": 103, "performance_name": "오페라 카르멘", "actual": 2500, "predicted": float(preds[0]) - 80},
        {"performance_id": 104, "performance_name": "연극 연애혁명", "actual": 2900, "predicted": float(preds[0]) + 50},
        {"performance_id": 105, "performance_name": "무용 공연 불릿", "actual": 2700, "predicted": float(preds[0]) - 30}
    ]
    
    # 가상 시계열 데이터 (5일간의 누적 예측 및 신뢰구간)
    time_series_data = {
        "dates": ["2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05"],
        "predicted_cumulative": [1000, 2000, float(preds[0]), float(preds[0]) + 150, float(preds[0]) + 300],
        "confidence_interval": {
            "lower": [950, 1900, float(preds[0]) - 20, float(preds[0]) + 130, float(preds[0]) + 280],
            "upper": [1050, 2100, float(preds[0]) + 20, float(preds[0]) + 170, float(preds[0]) + 320]
        }
    }
    
    # 가상 산점도 데이터 (예: 좌석 수 대비 예측 관객 수)
    capacity_scatter = {
        "data": [
            {"performance_id": 101, "capacity": 500, "predicted_sales": float(preds[0]), "genre": "뮤지컬"},
            {"performance_id": 102, "capacity": 750, "predicted_sales": float(preds[0]) + 50, "genre": "뮤지컬"},
            {"performance_id": 103, "capacity": 600, "predicted_sales": float(preds[0]) - 30, "genre": "뮤지컬"}
        ]
    }
    
    return {
        "predictions": preds.tolist(),
        "comparison": {"performances": comparison_data},
        "capacity_scatter": capacity_scatter,
        "time_series": time_series_data
    }

# 2) 회귀: 관객 수 예측 - 판매 단계
def predict_acc_sales_selling(input_data: List[dict]) -> dict:
    """
    모델 파일: xgb_reg_accumulated_sales_selling.pkl
    - 판매 단계에서는 실제 판매 데이터와 예측 데이터를 비교할 수 있는
      시계열 데이터, 좌석 수 산점도, 유사 공연 비교 데이터를 가상으로 생성합니다.
    """
    model = load_model("xgb_reg_accumulated_sales_selling")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    
    time_series_data = {
        "dates": ["2025-06-01", "2025-06-02", "2025-06-03", "2025-06-04"],
        "actual_cumulative": [1100, 2000, 3000, float(preds[0])],
        "predicted_cumulative": [1150, 2050, 3100, float(preds[0])]
    }
    
    capacity_scatter = {
        "data": [
            {"performance_id": 201, "capacity": 500, "accumulated_sales": float(preds[0])},
            {"performance_id": 202, "capacity": 750, "accumulated_sales": float(preds[0]) - 100},
            {"performance_id": 203, "capacity": 600, "accumulated_sales": float(preds[0]) + 50}
        ]
    }
    
    comparison_data = [
        {"performance_id": 201, "performance_name": "뮤지컬 캣츠", "actual": 1200, "predicted": float(preds[0])},
        {"performance_id": 202, "performance_name": "콘서트 아이유", "actual": 950, "predicted": float(preds[0]) - 40},
        {"performance_id": 203, "performance_name": "오페라 카르멘", "actual": 1100, "predicted": float(preds[0]) + 30}
    ]
    
    return {
        "predictions": preds.tolist(),
        "time_series": time_series_data,
        "capacity_scatter": capacity_scatter,
        "comparison": {"performances": comparison_data}
    }

# 3) 회귀: 손익 예측(ROI, BEP) - 기획 단계
def predict_roi_bep_planning(input_data: List[dict]) -> dict:
    """
    모델 파일: xgb_reg_roi_bep_planning.pkl
    - 기획 단계에서는 예측된 ROI와 BEP와 함께, 총매출, 총비용 등 파생 지표를 가상으로 반환합니다.
    """
    model = load_model("xgb_reg_roi_bep_planning")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    
    roi_bep_detail = {
        "total_revenue": 35000000,
        "total_cost": 42000000,
        "fixed_cost": 60000000,
        "variable_cost_rate": 0.2
    }
    
    roi_time_series = {
        "dates": ["시뮬레이션1", "시뮬레이션2", "시뮬레이션3", "시뮬레이션4", "시뮬레이션5"],
        "roi_values": [-0.85, -0.84, -0.83, float(preds[0][0]), -0.86]
    }
    
    roi_distribution = {
        "roi_values": [-0.85, -0.84, -0.83, float(preds[0][0]), -0.86],
        "bep_values": [3400, 3410, 3420, float(preds[0][1]), 3430]
    }
    
    return {
        "predictions": preds.tolist(),
        "roi_bep_detail": roi_bep_detail,
        "roi_time_series": roi_time_series,
        "roi_distribution": roi_distribution
    }

# 4) 회귀: 손익 예측(ROI, BEP) - 판매 단계
def predict_roi_bep_selling(input_data: List[dict]) -> dict:
    """
    모델 파일: xgb_reg_roi_bep_selling.pkl
    - 판매 단계에서는 실제 판매 데이터와 예측 손익 지표를 비교할 수 있는 추가 가상 데이터를 포함하여 반환합니다.
    """
    model = load_model("xgb_reg_roi_bep_selling")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    
    comparison_data = {
        "actual": {
            "accumulated_sales": 50000,
            "total_revenue": 40000000,
            "total_cost": 45000000
        },
        "predicted": {
            "accumulated_sales": 50000,
            "roi": float(preds[0][0]),
            "bep": float(preds[0][1])
        }
    }
    
    time_series_data = {
        "dates": ["2025-07-01", "2025-07-02", "2025-07-03"],
        "actual_cumulative": [15000, 35000, 50000],
        "predicted_cumulative": [15500, 36000, 50000],
        "confidence_interval": {
            "lower": [15000, 34000, 48000],
            "upper": [16000, 37000, 52000]
        }
    }
    
    return {
        "predictions": preds.tolist(),
        "comparison": comparison_data,
        "time_series": time_series_data
    }

# 5) 분류: 티켓 판매 위험 예측 - 판매 단계 (조기 경보)
def predict_ticket_risk(input_data: List[dict]) -> dict:
    """
    모델 파일: rf_cls_ticket_risk.pkl
    - 판매 단계 티켓 위험 예측 시, booking_rate를 기준으로 위험도를 세분화하여 경고 텍스트와
      현실적인 공연명 및 비교 데이터를 반환합니다.
    """
    model = load_model("rf_cls_ticket_risk")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    
    booking_rate = input_data[0].get("booking_rate", 0)
    # 조건에 따른 위험도 평가 텍스트 (세분화)
    if booking_rate >= 75:
        warning_text = "안정 (저위험)"
    elif booking_rate >= 60:
        warning_text = "중위험"
    else:
        warning_text = "고위험"
    
    performance_list = [
        {"performance_id": 301, "performance_name": "뮤지컬 캣츠", "actual_booking_rate": 78, "predicted_risk": int(preds[0])},
        {"performance_id": 302, "performance_name": "콘서트 아이유", "actual_booking_rate": 65, "predicted_risk": int(preds[0])},
        {"performance_id": 303, "performance_name": "오페라 카르멘", "actual_booking_rate": 55, "predicted_risk": int(preds[0])},
        {"performance_id": 304, "performance_name": "연극 연애혁명", "actual_booking_rate": 62, "predicted_risk": int(preds[0])},
        {"performance_id": 305, "performance_name": "무용 공연 불릿", "actual_booking_rate": 60, "predicted_risk": int(preds[0])}
    ]
    
    time_series_data = {
        "dates": ["2025-08-01", "2025-08-02", "2025-08-03"],
        "booking_rate": [58, 57, 56],
        "target_booking_rate": 75
    }
    
    return {
        "risk_labels": preds.tolist(),
        "risk_detail": {
            "current_booking_rate": booking_rate,
            "target_booking_rate": 75,
            "warning": warning_text
        },
        "performance_list": performance_list,
        "time_series": time_series_data
    }
