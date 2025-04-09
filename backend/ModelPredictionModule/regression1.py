import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# 1) 데이터 불러오기
performance_df = pd.read_csv('data/performance_tb.csv')
sales_df = pd.read_csv('data/sales_tb.csv')

# --------------------------------------------------
# 예시) performance_id를 기준으로 Join (환경에 맞게 수정하세요)
# --------------------------------------------------
df = pd.merge(performance_df, sales_df, on='performance_id', how='inner')

# 2) 분석에 사용할 피처(X)와 예측 대상(y) 정의
# ※ 실제로는 필요한 전처리/결측치 처리 등이 추가될 수 있습니다.
feature_cols = [
    'genre',               # 범주형
    'region',              # 범주형
    'start_date',          # 날짜 -> 필요 시 전처리(예: 일수 변환)
    'capacity',            # 수치형
    'star_power',          # 수치형
    'ticket_price',        # 수치형
    'marketing_budget',    # 수치형
    'sns_mention_count',   # 수치형
    'daily_sales',         # 수치형
    'booking_rate',        # 수치형
    'ad_exposure',         # 수치형
    'sns_mention_daily'    # 수치형
]
X = df[feature_cols]
y = df['accumulated_sales']  # 누적 판매 티켓 수(목표)

# 3) 범주형/수치형 데이터 전처리
# 예: 장르(genre), 지역(region) 등은 OneHotEncoder 사용
categorical_features = ['genre', 'region']
numerical_features   = list(set(feature_cols) - set(categorical_features))

# ColumnTransformer로 전처리 파이프라인 구성
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        # 수치형에는 별도 스케일링이 필요하다면 추가 (StandardScaler 등)
        ('num', 'passthrough', numerical_features)
    ]
)

# 4) 모델 구성(파이프라인)
model = Pipeline([
    ('preprocessing', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 5) 학습 데이터 분할 및 모델 학습
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# 6) 모델 평가(간단 예시: R^2 점수)
r2_score = model.score(X_test, y_test)
print(f"[관객 수 예측: RandomForest] Test R^2 Score: {r2_score:.4f}")

# 7) 모델 저장(models 디렉터리)
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/rf_reg_accumulated_sales.pkl')
print(">>> 모델이 'models/rf_reg_accumulated_sales.pkl' 로 저장되었습니다.")
