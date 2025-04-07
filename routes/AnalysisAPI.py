from fastapi import APIRouter, UploadFile
from backend.AzureServiceModule.TextAnalysis import TextAnalytics
from backend.AzureServiceModule.DocumentAnalysis import DocumentAnalysis

router = APIRouter()
text_analyzer = TextAnalytics()
document_analyzer = DocumentAnalysis()

@router.post("/analyze-review")
def analyze_review(text: str):
    return text_analyzer.analze_review(text)

@router.post("/analyze-doc")
async def analyze_document(file: UploadFile):
    content = await file.read()
    text = document_analyzer.analyze_document(content)
    return {"text": text}  # 예시