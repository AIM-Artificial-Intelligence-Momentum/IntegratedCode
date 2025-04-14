from AzureServiceModule.modules.AzureOpenAIClient import get_azure_openai_client
from AzureServiceModule.modules.IntentClassifier import IntentClassifier
from AzureServiceModule.modules.StageDetector import StageDetector
from AzureServiceModule.modules.VariableExtractor import AITextExtractor
from AzureServiceModule.modules.PromptGenerator import PromptGenerator
from AzureServiceModule.modules.AISearchClient import AISearchService
from AzureServiceModule.config.VariableConfig import required_keys, categorical_keys
import json

class ChatbotService:
    def __init__(self, api_key, endpoint, deployment, search_key, search_endpoint, search_index):
        # Azure OpenAI 클라이언트 초기화
        self.client = get_azure_openai_client(api_key, endpoint)
        self.deployment = deployment
        
        # 4가지 핵심 기능 초기화
        self.extractor = AITextExtractor(self.client, self.deployment, required_keys, categorical_keys)  # JSON 변수 추출기
        self.prompter = PromptGenerator(self.client, self.deployment, categorical_keys)                  # 챗봇 질문 생성기
        self.search = AISearchService(self.client, self.deployment, search_key, search_endpoint, search_index)  # 문서 검색기
        self.detector = StageDetector(self.client, self.deployment)
        self.classifier = IntentClassifier(self.client, self.deployment)

        # 상태 정보
        self.collected_vars = {}
        self.last_asked_key = None

    async def handle_user_input(self, user_input, history):
        if not isinstance(history, list):
            history = []

        # 1. 사용자 의도 분류: 수집 / 검색 / 혼합
        intent = self.classifier.classify_intent(user_input)
        reply_parts = []

        # 2-1. JSON 변수 수집
        if intent in ["수집", "혼합"]:
            extracted = self.extractor.extract_variables(user_input, fallback_key=self.last_asked_key)
            for key, val in extracted.items():
                if val is not None:
                    self.collected_vars[key] = val

            # 2-2. 추가 유도 질문 생성
            stage = self.detector.detect_stage(user_input)
            next_question, next_key = self.prompter.generate(self.collected_vars, user_input, stage)
            if next_key:
                self.last_asked_key = next_key
            reply_parts.append(next_question)

        # 3. AI 문서 검색
        if intent in ["검색", "혼합"]:
            summary = self.search.query(user_input)
            reply_parts.append("📖 관련 문서 요약:\n\n" + summary)

        # 4. 응답 및 상태 반환
        full_reply = "\n\n".join(reply_parts)
        history.append((user_input, full_reply))
        current_state = json.dumps(self.collected_vars, indent=2, ensure_ascii=False)

        return {
            "chat_history": history, # 전체 사용자, 챗봇 히스토리 출력 
            "response_text": full_reply, # 챗봇 응답만 출력
            "structured_data": self.collected_vars, # 모인 JSON 변수 
        }
# 'structured_data': 
# {'genre': ' 뮤지컬', 
#  'region': '부산광역시', 
#  'start_date': '2025-05-03', 
#  'capacity': 500, 
#  'star_power': 3}}
