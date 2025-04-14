import os
import joblib
import pandas as pd
import numpy as np
from typing import List
from sklearn.metrics import roc_curve, precision_recall_curve
from sklearn.preprocessing import label_binarize

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
    
    comparison_data = [
        {"performance_id": 101, "performance_name": "뮤지컬 캣츠", "actual": 2800, "predicted": float(preds[0])},
        {"performance_id": 102, "performance_name": "콘서트 아이유", "actual": 3000, "predicted": float(preds[0]) + 120},
        {"performance_id": 103, "performance_name": "오페라 카르멘", "actual": 2500, "predicted": float(preds[0]) - 80},
        {"performance_id": 104, "performance_name": "연극 연애혁명", "actual": 2900, "predicted": float(preds[0]) + 50},
        {"performance_id": 105, "performance_name": "무용 공연 불릿", "actual": 2700, "predicted": float(preds[0]) - 30}
    ]
    
    time_series_data = {
        "dates": ["2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05"],
        "predicted_cumulative": [1000, 2000, float(preds[0]), float(preds[0]) + 150, float(preds[0]) + 300],
        "confidence_interval": {
            "lower": [950, 1900, float(preds[0]) - 20, float(preds[0]) + 130, float(preds[0]) + 280],
            "upper": [1050, 2100, float(preds[0]) + 20, float(preds[0]) + 170, float(preds[0]) + 320]
        }
    }
    
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
        {"performance_id": 201, "performance_name": "뮤지컬 이프댄", "actual": 1200, "predicted": float(preds[0])},
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

def compute_roc_pr(y_true, y_proba, num_classes=3):
    """
    y_true: 실제 레이블 배열 (예: [0, 1, 2, ...])
    y_proba: 모델이 반환한 예측 확률 (2D 배열, shape=(n_samples, num_classes))
    num_classes: 분류할 클래스 수 (여기서는 3)
    """
    y_true_bin = label_binarize(y_true, classes=list(range(num_classes)))
    roc_data = []
    pr_data = []
    for i in range(num_classes):
        fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_proba[:, i])
        precision, recall, _ = precision_recall_curve(y_true_bin[:, i], y_proba[:, i])
        roc_data.append({
            "class": i,
            "description": f"클래스 {i}에 대한 ROC Curve 데이터",
            "fpr": {
                "label": "False Positive Rate",
                "values": fpr.tolist()
            },
            "tpr": {
                "label": "True Positive Rate",
                "values": tpr.tolist()
            }
        })
        pr_data.append({
            "class": i,
            "description": f"클래스 {i}에 대한 Precision-Recall Curve 데이터",
            "precision": {
                "label": "Precision",
                "values": precision.tolist()
            },
            "recall": {
                "label": "Recall",
                "values": recall.tolist()
            }
        })
    return {"roc_curve": roc_data, "pr_curve": pr_data}


def predict_ticket_risk(input_data: List[dict]) -> dict:
    """
    모델 파일: rf_cls_ticket_risk.pkl
    - 판매 단계 티켓 위험 예측 시, booking_rate를 기준으로 위험도를 세분화하여 경고 텍스트와
      현실적인 공연명 및 비교 데이터를 반환합니다.
    - 추가로 ground truth가 있는 평가 데이터셋(ticker_risk_ground_truth.csv)을 활용해
      ROC, PR Curve 데이터를 산출하여 시각화에 필요한 평가 데이터를 함께 반환합니다.
    """
    model = load_model("rf_cls_ticket_risk")
    df = pd.DataFrame(input_data)
    preds = model.predict(df)
    
    # 예측 확률 (predict_proba가 지원되는 경우)
    try:
        pred_proba = model.predict_proba(df)
    except Exception:
        pred_proba = np.full((df.shape[0], 3), 1/3)

    # 만약 예측 확률의 열 수가 3보다 작으면, 더미 데이터를 추가하여 3열로 맞춤
    if pred_proba.shape[1] < 3:
        if pred_proba.shape[1] == 1:
            # 이진 분류로 가정하고, 클래스 0 확률은 (1 - p), 클래스 2에 대해서는 0으로 채움
            prob_class0 = 1 - pred_proba[:, 0].reshape(-1, 1)
            prob_class1 = pred_proba
            prob_class2 = np.zeros((df.shape[0], 1))
            pred_proba = np.hstack([prob_class0, prob_class1, prob_class2])
        else:
            num_missing = 3 - pred_proba.shape[1]
            dummy = np.full((df.shape[0], num_missing), 1/3)
            pred_proba = np.hstack([pred_proba, dummy])

    # ground truth CSV 파일이 존재하면 사용, 없으면 dummy 데이터 생성 (샘플 수와 클래스 분포 개선)
    gt_local_path = os.path.join(FILE_DIR, "data", "ticket_risk_ground_truth.csv")
    if os.path.exists(gt_local_path):
        ground_truth_df = pd.read_csv(gt_local_path)
        y_true = ground_truth_df["risk_label"].values
    else:
        # 만약 입력 데이터의 샘플 수가 3 미만이면, 강제로 3개(0,1,2)를 사용하고,
        # pred_proba도 3개의 샘플로 확장합니다.
        if df.shape[0] < 3:
            y_true = np.array([0, 1, 2])
            pred_proba = np.vstack([pred_proba[0]] * 3)
        else:
            # 입력 데이터의 샘플 수(n)를 균등 분포하도록 0,1,2가 반복되도록 생성
            n = df.shape[0]
            repeats = int(np.ceil(n / 3))
            y_true = np.tile(np.array([0, 1, 2]), repeats)[:n]

    evaluation_curves = compute_roc_pr(y_true, pred_proba, num_classes=3)
    
    # booking_rate 기반 위험도 평가
    booking_rate = input_data[0].get("booking_rate", 0)
    if booking_rate >= 75:
        warning_text = "안정 (저위험)"
    elif booking_rate >= 60:
        warning_text = "중위험"
    else:
        warning_text = "고위험"
    
    performance_list = [
        {"performance_id": 301, "performance_name": "뮤지컬 이프댄", "actual_booking_rate": 78, "predicted_risk": int(preds[0])},
        {"performance_id": 302, "performance_name": "콘서트 아이유", "actual_booking_rate": 65, "predicted_risk": int(preds[0])},
        {"performance_id": 303, "performance_name": "오페라 카르멘", "actual_booking_rate": 55, "predicted_risk": int(preds[0])},
        {"performance_id": 304, "performance_name": "연극 굿모닝 홍콩", "actual_booking_rate": 62, "predicted_risk": int(preds[0])},
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
        "time_series": time_series_data,
        "evaluation_curves": evaluation_curves
    }

# -----------------------------
# 임시 더미 데이터를 반환하는 집계 시각화 함수들
# -----------------------------

def get_genre_stats() -> dict:
    """
    임시 더미 데이터를 반환하여 장르별 집계 시각화에 필요한 JSON 데이터를 생성합니다.
    원시 데이터 명세 (전처리 전): CSV 파일 '장르별 통계_20230101~20241231.csv'
      - 9개 장르 (예: "뮤지컬", "연극", "콘서트", "무용", "오페라", "발레", "재즈", "클래식", "다문화")
      - 각 장르별 총 공연작수, 누적 관객수, 티켓 매출액, 티켓 판매수 산출
    """
    result = {
        "genre_stats": {
            "genre": ["뮤지컬", "연극", "콘서트", "무용", "오페라", "발레", "재즈", "클래식", "다문화"],
            "performance_count": [120, 95, 80, 70, 65, 60, 55, 50, 45],
            "audience": [30000, 25000, 22000, 20000, 19000, 18000, 17000, 16000, 15000],
            "ticket_revenue": [50000000, 40000000, 35000000, 33000000, 32000000, 31000000, 30000000, 29000000, 28000000],
            "ticket_sales": [28000, 24000, 21000, 20500, 20000, 19500, 19000, 18500, 18000]
        }
    }
    return result

def get_regional_stats() -> dict:
    """
    임시 더미 데이터를 반환하여 지역별 집계 시각화에 필요한 JSON 데이터를 생성합니다.
    원시 데이터 명세 (전처리 전): CSV 파일 '지역별 통계_20230101~20241231.csv'
      - 상위 5개 지역 (예: "서울", "부산", "대구", "인천", "광주")
      - 각 지역별 공연건수, 상연횟수, 총 티켓판매수, 총 티켓매출액
    """
    result = {
        "regional_stats": {
            "region": ["서울", "부산", "대구", "인천", "광주"],
            "performance_count": [300, 150, 120, 100, 80],
            "show_count": [1000, 600, 500, 450, 300],
            "total_ticket_sales": [250000, 120000, 110000, 90000, 80000],
            "total_ticket_revenue": [75000000, 35000000, 33000000, 28000000, 25000000]
        }
    }
    return result

def get_venue_scale_stats() -> dict:
    """
    임시 더미 데이터를 반환하여 공연장 규모별 집계 시각화에 필요한 JSON 데이터를 생성합니다.
    원시 데이터 명세 (전처리 전): CSV 파일 '공연시설연도규모_분류.csv'
      - 연도와 규모 컬럼을 추가. 
      - 2023년 및 2024년 데이터 각각, 공연장 규모는 7개 범주:
            "좌석 미상", "1~300석 미만", "300~500석 미만", "500~1,000석 미만",
            "1,000~5,000석 미만", "5,000~10,000석 미만", "10,000석 이상"
      - 각 범주별 공연건수, 총 티켓판매수 산출
    """
    # 2023년 7개 범주 dummy 데이터
    year_2023 = [2023] * 7
    scales = ["좌석 미상", "1~300석 미만", "300~500석 미만", "500~1,000석 미만", "1,000~5,000석 미만", "5,000~10,000석 미만", "10,000석 이상"]
    perf_count_2023 = [100, 150, 120, 80, 60, 40, 20]         # 예시 값
    ticket_sales_2023 = [50000, 80000, 60000, 40000, 30000, 20000, 10000]
    
    # 2024년 7개 범주 dummy 데이터
    year_2024 = [2024] * 7
    perf_count_2024 = [110, 160, 130, 90, 70, 50, 30]            # 예시 값
    ticket_sales_2024 = [55000, 85000, 65000, 45000, 35000, 25000, 15000]
    
    # 합치기 (총 14개 항목)
    result = {
        "venue_scale_stats": {
            "year": year_2023 + year_2024,
            "scale": scales + scales,
            "performance_count": perf_count_2023 + perf_count_2024,
            "total_ticket_sales": ticket_sales_2023 + ticket_sales_2024
        }
    }
    return result