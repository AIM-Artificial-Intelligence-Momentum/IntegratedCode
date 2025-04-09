from backend.AzureServiceModule.AzureCLUClient import AzureCLUClient
from backend.AzureServiceModule.AzureOpenAIChat import AzureOpenAIChat

class ServiceRouter:
    def __init__(self):
        self.clu = AzureCLUClient()
        self.gpt = AzureOpenAIChat()

    def handle_user_input(self, user_input: str) -> dict:
        # CLU 분석
        clu_result = self.clu.analyze(user_input)
        intent = self.clu.get_top_intent(clu_result)
        entities = self.clu.get_entities(clu_result)

        # 의도 기반 시스템 프롬프트 결정
        system_prompt = self._get_system_prompt(intent, entities)

        # GPT 응답 생성
        gpt_result = self.gpt.run_conversation(prompt=user_input, history=[], system_prompt=system_prompt)

        return {
            "intent": intent,
            "entities": entities,
            "response": gpt_result
        }

    def _get_system_prompt(self, intent: str, entities: list) -> str:
        if intent == "공연_추천":
            return f"""너는 공연 기획을 돕는 GPT야.
            다음과 같은 정보를 기반으로 사용자가 공연을 기획할 수 있도록 도와줘.

            사용자의 의도는 '{intent}'이고, 추출된 정보는 다음과 같아: {entities}

            필요 시 추가 정보를 요청하거나 친절한 말투로 조언해줘."""

        elif intent == "공연_정보_질문":
            return "너는 공연 정보에 대해 답변하는 GPT야. 공연명, 장소, 시간 등을 알려줘."

        elif intent == "공연_예매_문의":
            return "너는 공연 예매 정보를 안내하는 GPT야. 예매 방법, 가격 등을 알려줘."

        else:
            return "너는 일반적인 질문에 답변해주는 GPT야."
