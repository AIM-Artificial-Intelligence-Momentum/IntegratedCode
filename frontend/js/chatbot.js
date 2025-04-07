// chatbot.js

const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");

// 메시지를 대화창에 추가하는 함수
function appendMessage(sender, text) {
  const message = document.createElement("div");
  message.style.marginBottom = "0.5rem";
  message.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatbox.appendChild(message);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// 메시지를 서버로 보내고 응답 받기
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("🙋‍♀️ You", message);
  userInput.value = "";

  try {
    const response = await fetch("/api/analysis/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) throw new Error("서버 응답 오류");

    const data = await response.json();
    appendMessage("🤖 Bot", data.reply || "응답이 없습니다.");
  } catch (err) {
    console.error(err);
    appendMessage("🤖 Bot", "⚠️ 오류가 발생했습니다. 서버를 확인해주세요.");
  }
}
