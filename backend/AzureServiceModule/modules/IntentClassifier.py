# AzureServiceModule/modules/IntentClassifier.py

class IntentClassifier:
    def __init__(self, client, deployment):
        self.client = client
        self.deployment = deployment

    # 사용자의 발화를 보고 intent 분류 (수집 / 검색 / 혼합 중 하나)
    def classify_intent(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": """
            다음 사용자의 발화가 어떤 목적에 해당하는지 분류하세요.

            - "수집" → 사용자가 공연 기획 관련 정보를 제공하고 있어, 추가 질문을 통해 변수를 수집해야 함
            - "검색" → 사용자가 무언가를 알려달라고 요청하고 있어, 문서 검색이 필요함
            - "혼합" → 일부 정보는 제공하고 있으나, 문서 검색을 통한 답변도 필요해 보임

            아래 중 하나만 출력하세요: 수집 / 검색 / 혼합
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