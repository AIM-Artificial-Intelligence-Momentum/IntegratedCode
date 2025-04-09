from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import CLUAnalysisAPI
from routes import MLAnalysisAPI

app = FastAPI()

# CORS 허용 (프론트에서 접근 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev 환경에서는 * 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes/analysis.py 파일 안에서 router = APIRouter()로 정의된 라우터 객체
# prefix="/api/analysis" : 이 라우터의 모든 경로 앞에 자동으로 /api/analysis가 붙음
app.include_router(CLUAnalysisAPI.router, prefix="/api/clu")

app.include_router(MLAnalysisAPI.router, prefix="/api/ml")

# 정적 파일 (D3.js 포함 프론트엔드)
app.mount("/static", StaticFiles(directory="frontend", html=True), name="frontend")