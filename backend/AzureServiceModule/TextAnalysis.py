import typing
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import asyncio
import os
from dotenv import load_dotenv

# 한국어는 Azure Text Analytics에 특화되어 있지 않음
# 대안 1 : Azure 대신 KoNLPy, Okt로 키워드 추출하기 
# 대안 2 : GPT로 번역해서 넘기기 
class TextAnalytics:
    def __init__(self):
        load_dotenv()

        self.endpoint_text = "https://6b028.cognitiveservices.azure.com/"
        self.key_text = os.getenv("TEXT_ANALYTICS_KEY")

        if self.key_text is None:
            raise ValueError("DOCUMENT_ANALYSIS_KEY is not set in the .env file")
        
        self.text_analytics_client = TextAnalyticsClient(
            endpoint=self.endpoint_text, 
            credential=AzureKeyCredential(self.key_text)
        )

    async def extract_keywords_async(self, sentences: typing.List[str]):
        """Azure Text Analytics로 문장 키워드 추출 (10개씩 분할 처리)"""
        async with self.text_analytics_client:
            batch_size = 10
            results = []

            for i in range(0, len(sentences), batch_size):
                batch = sentences[i:i + batch_size]
                response = await self.text_analytics_client.extract_key_phrases(batch)
                results.extend(response)

            return results

    async def analze_review(self, raw_text: str):
        """
        공연 리뷰 텍스트에서 핵심 키워드 추출
        param - raw_text: 여러 줄의 리뷰 텍스트
        return - {keyword: [관련 문장들]} 형태 딕셔너리
        """
        reviews = [sentence.strip() for sentence in raw_text.strip().split("\n") if sentence]
        results = await self.extract_keywords_async(reviews)

        keyword_map = {}
        print(results)
        for idx, result in enumerate(results):
            if not result.is_error:
                for phrase in result.key_phrases:
                    keyword_map.setdefault(phrase, [])
                    keyword_map[phrase].append(reviews[idx])

        return keyword_map