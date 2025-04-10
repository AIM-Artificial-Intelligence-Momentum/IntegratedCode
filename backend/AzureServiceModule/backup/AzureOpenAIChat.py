import requests
import os
from dotenv import load_dotenv

class AzureOpenAIChat:
    def __init__(self):
        load_dotenv()

        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("DEPLOYMENT_NAME")
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }

    def run_conversation(self, prompt: str, history: list = None, system_prompt: str = None) -> dict:
        if history is None:
            history = []
        print(history)

        messages = []

        # 시스템 프롬프트
        messages.append({
            "role": "system",
            "content": system_prompt or "You are an AI assistant that helps find information!"
        })

        # 이전 대화 히스토리 추가
        messages.extend(history)

        # 사용자 입력 추가
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

        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload)
            response.raise_for_status()  # 상태 코드가 200이 아니면 예외 발생

            result = response.json()

            if "choices" not in result or "message" not in result['choices'][0]:
                return {
                    "error": "GPT 응답 형식 오류",
                    "chat_history": history
                }

            bot_response = result['choices'][0]['message']['content'].strip()

            # 히스토리 업데이트
            updated_history = history.copy()
            updated_history.append({"role": "user", "content": prompt})
            updated_history.append({"role": "assistant", "content": bot_response})

            return {
                "bot_message": bot_response,
                "chat_history": updated_history
            }

        except requests.exceptions.RequestException as e:
            return {
                "error": f"[API 호출 오류] {str(e)}",
                "chat_history": history
            }

        except ValueError:
            return {
                "error": "[응답 JSON 파싱 실패]",
                "chat_history": history
            }
