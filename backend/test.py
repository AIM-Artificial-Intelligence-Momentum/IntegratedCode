import asyncio
import os
from dotenv import load_dotenv
from AzureServiceModule.ChatbotService import ChatbotService

load_dotenv()

# ✅ ChatbotService 인스턴스 생성
chatbot = ChatbotService(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    endpoint=os.getenv("ENDPOINT_URL"),
    deployment=os.getenv("DEPLOYMENT_NAME"),
    search_key=os.getenv("SEARCH_KEY"),
    search_endpoint=os.getenv("SEARCH_ENDPOINT"),
    search_index=os.getenv("SEARCH_INDEX_NAME")
)

async def interactive_test():
    print("🎭 공연 기획 챗봇 테스트 시작!")
    print("종료하려면 'exit' 입력\n")

    history = []

    while True:
        user_input = input("🙋 당신: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        result = await chatbot.handle_user_input(user_input, history)
        history = result["chat_history"]
        print('this is debug : ', result)

        print("\n🤖 챗봇 응답:")
        print(result["response_text"])

        print("\n📦 수집된 변수:")
        print(result["structured_data"])
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(interactive_test())
