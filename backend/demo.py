from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from routes  import MLAnalysisAPI
from routes import ChatbotAPI

app = FastAPI(docs_url="/api/docs")

# CORS 허용 (프론트에서 접근 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev 환경에서는 * 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(MLAnalysisAPI.router, prefix="/api/ml")
app.include_router(ChatbotAPI.router, prefix="/api/chabot")

