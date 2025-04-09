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
        print('this is clue_result', clu_result)
        print('this is intent', intent)
        print('this is entities', entities)

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
        basic_prompt = (
            f"당신은 공연 기획 전문가이자 친절한 챗봇입니다. "
            f"사용자의 의도는 '{intent}'이고, 현재까지 추출된 정보는 다음과 같습니다: {entities}.\n"
            f"이 정보를 바탕으로 필요한 수치를 도출하고, 누락된 정보는 자연스럽게 질문을 통해 보완해 주세요.\n"
        )

        if intent == "공연_추천":
            return basic_prompt + (
                "\n사용자가 원하는 공연 유형, 예산, 인원수 등을 고려해 적절한 공연 형태를 추천해 주세요.\n"
                "정보가 부족할 경우 추가로 물어봐 주시고, 기획에 도움이 될 수 있도록 친절하고 구체적인 조언을 제공해 주세요."
            )

        elif intent == "공연_정보_질문":
            return basic_prompt + (
                "\n사용자가 공연에 대해 알고 싶은 정보(예: 공연명, 장소, 시간 등)에 대해 정확하고 친절하게 설명해 주세요.\n"
                "가능하다면 관련 공연을 추천하거나 참고할 수 있는 사이트도 알려주세요."
            )

        elif intent == "공연_예매_문의":
            return basic_prompt + (
                "\n공연의 예매 방법, 가격, 좌석 정보 등을 구체적으로 안내해 주세요.\n"
                "예매 관련 플랫폼 링크나 절차도 함께 알려주면 좋아요."
            )

        elif intent == "공연_수익_예측":
            return basic_prompt + (
                "\n공연 수익을 예측하기 위해 필요한 정보(예: 관객 수, 티켓 가격, 회차 수, 대관료 등)를 확인하고 부족한 정보를 질문해 주세요.\n"
                "수익 예측을 위한 간단한 계산도 가능하다면 제공해 주세요."
            )

        else:
            return basic_prompt + (
                "\n일반적인 공연 관련 질문에 대해 성실하게 답변해 주세요.\n"
                "친근하고 예의 바른 말투를 유지해 주세요."
            )
