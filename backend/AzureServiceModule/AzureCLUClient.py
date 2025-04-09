import requests
import os
from dotenv import load_dotenv

class AzureCLUClient:
    def __init__(self):
        load_dotenv()

        self.endpoint = os.getenv("CLU_ENDPOINT")  # https://your-resource-name.cognitiveservices.azure.com
        self.api_key = os.getenv("CLU_KEY")
        self.project_name = os.getenv("CLU_PROJECT")
        self.deployment_name = os.getenv("CLU_DEPLOYMENT")

        if not all([self.endpoint, self.api_key, self.project_name, self.deployment_name]):
            raise ValueError("CLU 관련 환경변수가 누락되었습니다. .env 파일을 확인하세요.")

        self.api_url = self.endpoint

    def analyze(self, user_input: str) -> dict:
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            
            "Content-Type": "application/json"
        }

        body = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "id": "1",
                    "participantId": "user1",
                    "text": user_input,
                    "modality": "text",
                    "language": "ko"
                }
            },
            "parameters": {
                "projectName": self.project_name,
                "deploymentName": self.deployment_name,
                "verbose": True,
                "stringIndexType": "TextElement_V8"
            }
        }

        response = requests.post(self.api_url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()

    def get_top_intent(self, result: dict) -> str:
        return result["result"]["prediction"]["topIntent"]

    def get_entities(self, result: dict) -> list:
        return result["result"]["prediction"].get("entities", [])


