import requests
import os
from dotenv import load_dotenv

class AzureOpenAIChat:
    def __init__(self):
        load_dotenv()

        # 환경 변수에서 Azure OpenAI API 정보 로드
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("DEPLOYMENT_NAME")
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }

    def run_conversation(self, prompt: str, history: list = [], system_prompt: str = None) -> str:
        messages = []

        # 1. 시스템 프롬프트 설정
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        else:
            messages.append({
                "role": "system",
                "content": "You are an AI assistant that helps find information!"
            })

        # 2. 기존 대화 이력 추가
        for entry in history:
            messages.append(entry)

        # 3. 사용자 입력 추가
        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "messages": messages,
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 4096
        }

        response = requests.post(self.endpoint, headers=self.headers, json=payload)

        result = response.json()
        bot_response = result['choices'][0]['message']['content'].strip()

        return bot_response
