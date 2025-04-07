from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os
from dotenv import load_dotenv

class DocumentAnalysis:
    def __init__(self):
        # .env 파일에서 환경 변수를 로드
        load_dotenv()

        # .env 파일에 저장된 DOCUMENT_ANALYSIS_KEY를 환경 변수로 불러오기
        self.endpoint_doc = "https://6b028-document.cognitiveservices.azure.com/"
        self.key_doc = os.getenv("DOCUMENT_ANALYSIS_KEY")

        if self.key_doc is None:
            raise ValueError("DOCUMENT_ANALYSIS_KEY is not set in the .env file")

        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=self.endpoint_doc, credential=AzureKeyCredential(self.key_doc)
        )

    def analyze_document(self, file_path: str):
        """문서 분석을 통해 텍스트 추출"""
        with open(file_path, "rb") as f:
            poller = self.document_analysis_client.begin_analyze_document("prebuilt-read", f)
        
        result = poller.result()
        full_text = result.content
        return full_text
