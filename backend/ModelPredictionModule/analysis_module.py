# analysis_modules.py

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from typing import List

BASE_DIR = r"C:\Users\USER\Desktop\my_git\ml-analysis\ModelPredictionModule"

def load_model(model_name: str) -> Pipeline:
    """
    model_name 예) 'rf_reg_accumulated_sales', 'rf_reg_roi_bep',
                'rf_cls_ticket_risk', 'kmeans_audience_seg' ...
    pkl 파일을 로드하여 모델(Pipeline 등)을 반환한다.
    """
    file_path = os.path.join(BASE_DIR, model_name + ".pkl")
    model = joblib.load(file_path)
    return model

# ---------------------------
# 1) 회귀: 관객 수 예측
# ---------------------------
def predict_accumulated_sales(input_data: List[dict]) -> np.ndarray:
    """
    - input_data: [{feature1: val, feature2: val, ...}, ...]
    - return: 예측된 누적 판매량 (1차원 or 2차원 배열)
    """
    # 모델 로드
    model = load_model('rf_reg_accumulated_sales')
    
    # 입력을 DataFrame 변환
    df = pd.DataFrame(input_data)
    
    # 예측
    preds = model.predict(df)  # shape: (n_samples,)
    return preds

# ---------------------------
# 2) 회귀: 손익 예측 (ROI, BEP)
# ---------------------------
def predict_roi_bep(input_data: List[dict]) -> np.ndarray:
    """
    Multi-output 모델 (ROI, BEP) 동시 예측
    return shape: (n_samples, 2) => [[ROI_1, BEP_1], [ROI_2, BEP_2], ...]
    """
    model = load_model('rf_reg_roi_bep')
    df = pd.DataFrame(input_data)
    
    preds = model.predict(df)
    return preds

# ---------------------------
# 3) 분류: 티켓 판매 위험 예측
# ---------------------------
def predict_ticket_risk(input_data: List[dict]) -> np.ndarray:
    """
    티켓 판매 위험도 분류 (0=저위험, 1=중위험, 2=고위험)
    """
    model = load_model('rf_cls_ticket_risk')
    df = pd.DataFrame(input_data)
    
    risk_preds = model.predict(df)
    return risk_preds

# ---------------------------
# 4) 군집: 관객 세분화
# ---------------------------
def predict_audience_cluster(input_data: List[dict]) -> np.ndarray:
    """
    KMeans 군집화 -> cluster labels
    """
    model = load_model('kmeans_audience_seg')
    df = pd.DataFrame(input_data)
    
    clusters = model.predict(df)
    return clusters
