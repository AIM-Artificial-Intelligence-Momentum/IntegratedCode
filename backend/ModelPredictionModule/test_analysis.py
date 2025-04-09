# test_analysis.py

import pprint
from analysis_module import (
    predict_accumulated_sales,
    predict_roi_bep,
    predict_ticket_risk,
    predict_audience_cluster
)

# -------------------------------------------
# 더미 입력 데이터 준비
# -------------------------------------------

# 1) 회귀: 누적 판매 예측 입력 데이터 예시
dummy_acc_sales_input = [
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

# 2) 회귀: 손익 예측 (ROI, BEP) 입력 데이터 예시
dummy_roi_bep_input = [
    {
         "production_cost": 100000000,
         "marketing_budget": 50000000,
         "ticket_price": 80000,
         "capacity": 1000,
         "variable_cost_rate": 0.2,
         "accumulated_sales": 50000
    }
]

# 3) 분류: 티켓 판매 위험 예측 입력 데이터 예시
dummy_ticket_risk_input = [
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

# 4) 군집: 관객 세분화 입력 데이터 예시
dummy_audience_cluster_input = [
    {
         "booking_count": 5,
         "total_amount": 500000,
         "age": 35,
         "recency_days" : 30
    }
]

# -------------------------------------------
# 각 함수 테스트
# -------------------------------------------

print("=== Testing predict_accumulated_sales ===")
pred_acc_sales = predict_accumulated_sales(dummy_acc_sales_input)
pprint.pprint(pred_acc_sales)  # 예: array([12345.6789])

print("\n=== Testing predict_roi_bep ===")
pred_roi_bep = predict_roi_bep(dummy_roi_bep_input)
pprint.pprint(pred_roi_bep)  # 예: array([[0.35, 7543]])

print("\n=== Testing predict_ticket_risk ===")
pred_ticket_risk = predict_ticket_risk(dummy_ticket_risk_input)
pprint.pprint(pred_ticket_risk)  # 예: array([0]) 또는 array([1,2] ...)

print("\n=== Testing predict_audience_cluster ===")
pred_audience_cluster = predict_audience_cluster(dummy_audience_cluster_input)
pprint.pprint(pred_audience_cluster)  # 예: array([1]) 또는 array([0,2,1] ...)
