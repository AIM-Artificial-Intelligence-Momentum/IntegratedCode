<<<<<<< HEAD
import requests
import json

url = "http://127.0.0.1:8000/api/ml/accumulated_sales"
data = [
=======
# test_analysis.py

import pprint
from analysis_module import (
    predict_acc_sales_planning,
    predict_acc_sales_selling,
    predict_roi_bep_planning,
    predict_roi_bep_selling,
    predict_ticket_risk_early,
    predict_audience_cluster
)

# -------------------------------------------
# 더미 입력 데이터 준비 (새 분석 시나리오 반영)
# -------------------------------------------

# 1) 관객 수 예측 - 기획 단계
dummy_acc_sales_planning_input = [
    {
        "genre": "뮤지컬",
        "region": "서울",
        "start_date_numeric": 1800,
        "capacity": 500,
        "star_power": 4,
        "ticket_price": 80000,
        "marketing_budget": 1000000,
        "sns_mention_count": 3000
        # 판매 단계에 필요한 daily_sales, booking_rate 등은 없음
    }
]

# 2) 관객 수 예측 - 판매 단계
dummy_acc_sales_selling_input = [
>>>>>>> origin/main
    {
        "genre": "뮤지컬",
        "region": "서울",
        "start_date_numeric": 1800,
        "capacity": 500,
        "star_power": 4,
        "ticket_price": 80000,
        "marketing_budget": 1000000,
        "sns_mention_count": 3000,
        "daily_sales": 100,
        "booking_rate": 65,
        "ad_exposure": 2000,
        "sns_mention_daily": 50
    }
]

<<<<<<< HEAD
headers = {"Content-Type": "application/json"}
response = requests.post(url, data=json.dumps(data), headers=headers)

print("응답 코드:", response.status_code)
print("응답 텍스트:", response.text)
print("응답 내용:", response.json())
=======
# 3) 손익 예측(ROI, BEP) - 기획 단계
dummy_roi_bep_planning_input = [
    {
        "production_cost": 100000000,
        "marketing_budget": 50000000,
        "ticket_price": 80000,
        "capacity": 1000,
        "variable_cost_rate": 0.2
        # accumulated_sales는 기획 단계에서는 제공되지 않음
    }
]

# 4) 손익 예측(ROI, BEP) - 판매 단계
dummy_roi_bep_selling_input = [
    {
        "production_cost": 100000000,
        "marketing_budget": 50000000,
        "ticket_price": 80000,
        "capacity": 1000,
        "variable_cost_rate": 0.2,
        "accumulated_sales": 50000
    }
]

# 5) 티켓 판매 위험 예측 - 판매 단계 조기 경보
dummy_ticket_risk_early_input = [
    {
        "genre": "콘서트",
        "region": "부산",
        "start_date_numeric": 1900,
        "capacity": 600,
        "star_power": 5,
        "daily_sales": 80,
        "accumulated_sales": 300,
        "ad_exposure": 2500,
        "sns_mention_daily": 60,
        "promo_event_flag": 1
    }
]

# 6) 관객 세분화 (군집)
dummy_audience_cluster_input = [
    {
        "booking_count": 5,
        "total_amount": 500000,
        "age": 35,
        "recency_days": 30
    }
]

# -------------------------------------------
# 각 함수 테스트
# -------------------------------------------

print("=== (회귀) 관객 수 예측 - 기획 단계 ===")
res1 = predict_acc_sales_planning(dummy_acc_sales_planning_input)
pprint.pprint(res1)

print("\n=== (회귀) 관객 수 예측 - 판매 단계 ===")
res2 = predict_acc_sales_selling(dummy_acc_sales_selling_input)
pprint.pprint(res2)

print("\n=== (회귀) 손익 예측(ROI, BEP) - 기획 단계 ===")
res3 = predict_roi_bep_planning(dummy_roi_bep_planning_input)
pprint.pprint(res3)

print("\n=== (회귀) 손익 예측(ROI, BEP) - 판매 단계 ===")
res4 = predict_roi_bep_selling(dummy_roi_bep_selling_input)
pprint.pprint(res4)

print("\n=== (분류) 티켓 판매 위험 예측 - 판매 단계 조기 경보 ===")
res5 = predict_ticket_risk_early(dummy_ticket_risk_early_input)
pprint.pprint(res5)

print("\n=== (군집) 관객 세분화 ===")
res6 = predict_audience_cluster(dummy_audience_cluster_input)
pprint.pprint(res6)
>>>>>>> origin/main
