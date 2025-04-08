from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
import os
from dotenv import load_dotenv

class AzureCLUClient:
    def __init__(self):
        load_dotenv()

        self.endpoint = os.getenv("CLU_ENDPOINT")
        self.key = os.getenv("CLU_KEY")
        self.project_name = os.getenv("CLU_PROJECT")
        self.deployment_name = os.getenv("CLU_DEPLOYMENT")

        if not all([self.endpoint, self.key, self.project_name, self.deployment_name]):
            raise ValueError("CLU 관련 환경변수가 누락되었습니다. .env 파일을 확인하세요.")

        self.client = ConversationAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

    def analyze(self, user_input: str) -> dict:
        """
        CLU로 사용자 입력을 분석하여 intent + entities 반환
        """
        result = self.client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "id": "1",
                        "participantId": "user1",
                        "text": user_input
                    },
                    "modality": "text",
                    "language": "ko"
                },
                "parameters": {
                    "projectName": self.project_name,
                    "deploymentName": self.deployment_name,
                    "verbose": True
                }
            }
        )
        return result

    def get_top_intent(self, result: dict) -> str:
        """
        CLU 결과에서 가장 높은 Intent 반환
        """
        return result["result"]["prediction"]["topIntent"]

    def get_entities(self, result: dict) -> list:
        """
        CLU 결과에서 Entity 리스트 반환
        """
        return result["result"]["prediction"].get("entities", [])
