import gradio as gr
import requests
import json

API_URL = "http://localhost:8000/api/aisearch/route"
chat_history = []

def call_fastapi(input_text):
    global chat_history
    payload = {
        "input": input_text,
        "history": chat_history
    }

    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        chat_history = data["history"]
        structured_data = data.get("structured_data", {})
        citations = data.get("citations", [])

        # (user, assistant) 튜플로 묶기
        messages = []
        buffer = {}
        for h in chat_history:
            if h["role"] == "user":
                buffer["user"] = h["content"]
            elif h["role"] == "assistant" and "user" in buffer:
                messages.append((buffer["user"], h["content"]))
                buffer = {}

        return (
            messages,
            json.dumps(structured_data, ensure_ascii=False, indent=2),
            "\n".join(citations),
            ""
        )
    else:
        return [], "❌ 오류: " + response.text, "", ""

with gr.Blocks() as demo:
    gr.Markdown("🎭 **FastAPI 연동 테스트 (공연 기획 챗봇)**")

    chatbot = gr.Chatbot(label="💬 대화 히스토리")
    structured_box = gr.Textbox(label="📦 구조화 데이터(JSON)", lines=8)
    citations_box = gr.Textbox(label="📚 참조 자료(Citations)", lines=6)
    txt = gr.Textbox(show_label=False, placeholder="메시지를 입력하세요...")

    txt.submit(call_fastapi, [txt], [chatbot, structured_box, citations_box, txt])

if __name__ == "__main__":
    demo.launch(share=True)
