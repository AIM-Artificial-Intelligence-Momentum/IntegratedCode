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
def predict_acc_sales_planning(input_data: List[dict]) -> np.ndarray:
    """
    모델 파일: xgb_reg_accumulated_sales_planning.pkl
    """
    model = load_model("xgb_reg_accumulated_sales_planning")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    return preds

# 2) 회귀: 관객 수 예측 - 판매 단계
def predict_acc_sales_selling(input_data: List[dict]) -> np.ndarray:
    """
    모델 파일: xgb_reg_accumulated_sales_selling.pkl
    """
    model = load_model("xgb_reg_accumulated_sales_selling")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    return preds

# 3) 회귀: 손익 예측(ROI, BEP) - 기획 단계
def predict_roi_bep_planning(input_data: List[dict]) -> np.ndarray:
    """
    모델 파일: xgb_reg_roi_bep_planning.pkl
    """
    model = load_model("xgb_reg_roi_bep_planning")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    return preds

# 4) 회귀: 손익 예측(ROI, BEP) - 판매 단계
def predict_roi_bep_selling(input_data: List[dict]) -> np.ndarray:
    """
    모델 파일: xgb_reg_roi_bep_selling.pkl
    """
    model = load_model("xgb_reg_roi_bep_selling")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    return preds

# 5) 분류: 티켓 판매 위험 예측 - 판매 단계
def predict_ticket_risk(input_data: List[dict]) -> np.ndarray:
    """
    모델 파일: rf_cls_ticket_risk.pkl
    """
    model = load_model("rf_cls_ticket_risk")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    return preds

# 6) 군집: 관객 세분화
def predict_audience_cluster(input_data: List[dict]) -> np.ndarray:
    """
    모델 파일: kmeans_audience_seg.pkl
    """
    model = load_model("kmeans_audience_seg")
    df = pd.DataFrame(input_data)
    clusters = model.predict(df)
    return clusters
