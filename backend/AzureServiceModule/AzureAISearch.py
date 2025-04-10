from dotenv import load_dotenv
import os
import requests
import re
import json

load_dotenv()

# 환경변수 설정
CHAT_ENDPOINT = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AI_SEARCH_ENDPOINT = os.getenv("AI_SEARCH_ENDPOINT")
AI_SEARCH_API_KEY = os.getenv("AI_SEARCH_API_KEY")
AI_SEARCH_INDEX = os.getenv("AI_SEARCH_INDEX")
AI_SEARCH_SEMANTIC = os.getenv("AI_SEARCH_SEMANTIC")

# 수익 예측용 변수 클래스
class RevenueForecast:
    def __init__(self):
        self.data = {
            "show_name": "",
            "show_period": "",
            "location": "",
            "target_audience": 0,
            "predicted_revenue": "",
            "estimated_cost": "",
            "performers": "",
            "marketing_breakdown": [],
            "audience_trend": []
        }

    def update(self, new_data):
        for key, value in new_data.items():
            if key in self.data and value:
                self.data[key] = value

    def to_dict(self):
        return self.data

# 시스템 프롬프트
system_prompt = (
    "당신은 공연 기획 전문가이자 친절한 챗봇입니다.\n"
    "다음 클래스에 해당하는 매개변수 값을 사용자로부터 얻고, 매 응답마다 업데이트하세요.\n"
    "class 수익예측:\n"
    "    공연명(show_name), 기간(show_period), 장소(location), 예상 관객수(target_audience),\n"
    "    예상 수익(predicted_revenue), 예상 비용(estimated_cost), 출연진(performers),\n"
    "    마케팅 비율(marketing_breakdown: category와 value 포함), 관객 추이(audience_trend: 숫자 리스트)\n\n"
    "응답은 친절한 설명형 텍스트만 포함하세요. 그러나 반드시 응답 **마지막에** 아래 JSON 구조를 포함하세요:\n\n"
    "{\"show_name\": ..., \"show_period\": ..., ...}\n\n"
    "이 JSON은 시스템에서만 사용되며, 사용자에게는 표시되지 않습니다. 코드 블록(```) 없이 텍스트로만 넣으세요."
)


class ServiceRouter:
    def __init__(self):
        self.chat_history = []
        self.revenue_forecast = RevenueForecast()

    def request_gpt(self, prompt):
        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY
        }

        messages = [{"role": "system", "content": system_prompt}]
        for msg in self.chat_history:
            messages.append(msg)
        messages.append({"role": "user", "content": prompt})

        body = {
            "messages": messages,
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 1000,
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": AI_SEARCH_ENDPOINT,
                        "index_name": AI_SEARCH_INDEX,
                        "semantic_configuration": AI_SEARCH_SEMANTIC,
                        "query_type": "semantic",
                        "fields_mapping": {},
                        "in_scope": True,
                        "filter": None,
                        "strictness": 1,
                        "top_n_documents": 3,
                        "authentication": {
                            "type": "api_key",
                            "key": AI_SEARCH_API_KEY
                        }
                    }
                }
            ]
        }

        response = requests.post(CHAT_ENDPOINT, headers=headers, json=body)

        if response.status_code != 200:
            return {
                "response": "❌ 오류: GPT 호출 실패",
                "extracted_json": self.revenue_forecast.to_dict(),
                "citations": []
            }

        response_json = response.json()
        message = response_json['choices'][0]['message']
        content = message['content']
        content = re.sub(r'\[doc(\d+)\]', r'[참조 \1]', content)

        # JSON 추출 시도
        extracted_json = {}
        try:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            print("📦 추출된 content:\n",content)
            if json_match:
                json_block = json_match.group()
                print("📦 추출된 JSON 블록:\n", json_block)
                extracted_json = json.loads(json_block)
                content = content.replace(json_block, "").strip()
        except Exception as e:
            print("❌ JSON 추출 실패:", e)

        self.revenue_forecast.update(extracted_json)

        # citation 추출
        citations = []
        if "context" in message and "citations" in message["context"]:
            for i, cite in enumerate(message["context"]["citations"]):
                excerpt = cite.get("content", "").replace("\n", " ")[:200]
                citations.append(f"📌[참조 {i+1}] {excerpt}...\n")

        # 채팅 히스토리 업데이트
        self.chat_history.append({"role": "user", "content": prompt})
        self.chat_history.append({"role": "assistant", "content": content})

        return {
            "response": content,
            "extracted_json": self.revenue_forecast.to_dict(),
            "citations": citations
        }

    async def handle_user_input(self, prompt, history):
        result = self.request_gpt(prompt)
        return {
            "history": self.chat_history,
            "structured_data": result["extracted_json"],
            "citations": result["citations"]
        }