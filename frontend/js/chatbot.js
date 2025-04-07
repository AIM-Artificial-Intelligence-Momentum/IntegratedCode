const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");

let chatHistory = [];

// 메시지 추가 함수
function appendMessage(sender, text) {
  const message = document.createElement("div");
  message.style.marginBottom = "0.5rem";
  message.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatbox.appendChild(message);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// 서버로 메시지 전송
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("🙋‍♀️ You", message);
  userInput.value = "";

  try {
    const response = await fetch("/api/chatbot/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        prompt: message,
        history: chatHistory
      })
    });

    if (!response.ok) throw new Error("서버 응답 오류");

    const data = await response.json();
    appendMessage("🤖 Bot", data.reply);
    chatHistory = data.history;
  } catch (err) {
    console.error(err);
    appendMessage("🤖 Bot", "⚠️ 오류가 발생했습니다.");
  }
}
