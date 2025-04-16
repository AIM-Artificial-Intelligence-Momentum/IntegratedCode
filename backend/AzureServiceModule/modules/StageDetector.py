# AzureServiceModule/modules/StageDetector.py

class StageDetector:
    def __init__(self, client, deployment):
        self.client = client
        self.deployment = deployment
    # 사용자의 발화를 보고 기획 / 판매 단계 중 하나를 분류
    def detect_stage(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": """
            다음 사용자의 입력을 보고, 사용자가 공연의 어떤 단계에 있는지 분류하세요.
            - "기획" → 공연을 아직 준비 중이거나 초기 계획 단계
            - "판매" → 공연 기획은 끝났고, 지금은 판매와 마케팅 등 실행 단계

            두 선택지 중 하나만 출력하세요: 기획 / 판매
            """},
            {"role": "user", "content": user_input}
        ]

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=0,
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
