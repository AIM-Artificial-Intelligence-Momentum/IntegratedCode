const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");


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
    const response = await fetch("/api/clu/route", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        input: message,
      })
    });

    if (!response.ok) throw new Error("서버 응답 오류");
    console.log(response.text)
    const data = await response.json();

    // 응답 구성: intent, entities, response
    const intentMsg = `intent: ${data.intent}`;
    const entityMsg = data.entities.length ? `entities: ${data.entities.join(", ")}` : "";
    const botReply = `🤖 ${data.response}`;
    console.log(intentMsg)
    console.log(entityMsg)
    console.log(botReply)

    if (intentMsg) appendMessage("📡 System", intentMsg);
    if (entityMsg) appendMessage("📡 System", entityMsg);
    appendMessage("🤖 Bot", botReply);
  } catch (err) {
    console.error(err);
    appendMessage("🤖 Bot", "⚠️ 오류가 발생했습니다.");
  }
}
