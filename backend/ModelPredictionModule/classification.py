import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# 1) 데이터 불러오기
performance_df = pd.read_csv('data/performance_tb.csv')
sales_df = pd.read_csv('data/sales_tb.csv')
df = pd.merge(performance_df, sales_df, on='performance_id', how='inner')

# 2) start_date 컬럼을 datetime으로 변환 후, 기준 날짜로부터 경과 일수로 변환
df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
reference_date = pd.Timestamp("2020-01-01")
df['start_date_numeric'] = (df['start_date'] - reference_date).dt.days

# 원본 start_date 컬럼 삭제 (문자열 데이터가 남아있지 않도록)
df.drop(columns=['start_date'], inplace=True)

# 3) '위험도' 라벨 생성 (예시; 실제 기준에 맞게 수정)
# booking_rate >= 75: 저위험(0), 60 <= booking_rate < 75: 중위험(1), booking_rate < 60: 고위험(2)
def classify_risk(rate):
    if rate >= 75:
        return 0
    elif rate >= 60:
        return 1
    else:
        return 2

df['risk_label'] = df['booking_rate'].apply(classify_risk)

# 4) 피처와 타깃 정의 (start_date 대신 start_date_numeric 사용)
feature_cols = [
    'genre', 
    'region', 
    'start_date_numeric',  # 변환된 날짜 컬럼 사용
    'capacity', 
    'star_power', 
    'daily_sales', 
    'accumulated_sales', 
    'ad_exposure', 
    'sns_mention_daily', 
    'promo_event_flag'
]
X = df[feature_cols]
y = df['risk_label']

# 5) 범주형/수치형 데이터 전처리
categorical_features = ['genre', 'region', 'promo_event_flag']
numerical_features = list(set(feature_cols) - set(categorical_features))

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ]
)

# 6) 모델 구성 및 학습
model = Pipeline([
    ('preprocessing', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# 7) 평가 및 모델 저장
accuracy = model.score(X_test, y_test)
print(f"[티켓 판매 위험 예측] Accuracy: {accuracy:.4f}")

os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/rf_cls_ticket_risk.pkl')
print(">>> 모델이 'models/rf_cls_ticket_risk.pkl' 로 저장되었습니다.")
