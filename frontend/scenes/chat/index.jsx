// scenes/chat/index.jsx
"use client";

import { useState } from "react";
import {
  Box,
  IconButton,
  TextField,
  Paper,
  Typography,
  Divider,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import ChatIcon from "@mui/icons-material/Chat";
import CloseIcon from "@mui/icons-material/Close";

export default function ChatPage({ setPlanningSummary, setChartData }) {
  const [chatHistory, setChatHistory] = useState([
    {
      role: "assistant",
      content:
        "안녕하세요!\n\n 자유롭게 말씀해주세요.",
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const handleChat = async () => {
    if (!inputText.trim()) return;

    const updated = [...chatHistory, { role: "user", content: inputText }];
    setChatHistory(updated);
    setInputText("");

    try {
      const res = await fetch("http://localhost:8000/api/chatbot/response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          input: inputText,
          history: updated
            .filter((m) => m.role !== "system")
            .map(({ role, content }) =>
              role === "user" ? [content, ""] : ["", content]
            ),
        }),
      });

      if (!res.ok) throw new Error("API 응답 오류");

      const data = await res.json();

      // 결과 표시
      const botReply = data.response_text || "응답 없음";
      setChatHistory((prev) => [...prev, { role: "assistant", content: botReply }]);

      // 데이터 분석 결과 전달
      if (
        data.analysis_results &&
        data.analysis_results.accumulated_sales_planning &&
        typeof setChartData === "function"
      ) {
        setChartData(data.analysis_results.accumulated_sales_planning.predictions);
      }

      if (typeof setPlanningSummary === "function") {
        setPlanningSummary(data.analysis_results || {});
      }
    } catch (error) {
      console.error("채팅 요청 실패: ", error);
      setChatHistory((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ 서버 연결 중 오류가 발생했습니다.",
        },
      ]);
    }
  };

  return (
    <>
      {!isOpen && (
        <IconButton
          onClick={() => setIsOpen(true)}
          sx={{
            position: "fixed",
            bottom: 20,
            right: 20,
            zIndex: 1500,
            bgcolor: "primary.main",
            color: "white",
            "&:hover": { bgcolor: "primary.dark" },
          }}
        >
          <ChatIcon />
        </IconButton>
      )}

      {isOpen && (
        <Paper
          elevation={3}
          sx={{
            position: "fixed",
            bottom: 20,
            right: 20,
            width: 360,
            height: "80vh",
            display: "flex",
            flexDirection: "column",
            zIndex: 1500,
          }}
        >
          <Box
            sx={{
              p: 2,
              borderBottom: "1px solid #ddd",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Typography fontWeight="bold">Chat with DM</Typography>
            <IconButton size="small" onClick={() => setIsOpen(false)}>
              <CloseIcon fontSize="small" />
            </IconButton>
          </Box>

          <Box
            sx={{
              flex: 1,
              overflowY: "auto",
              p: 2,
              bgcolor: "#f3f3f3",
              display: "flex",
              flexDirection: "column",
              gap: 1,
            }}
          >
            {chatHistory.map((msg, idx) => (
              <Box
                key={idx}
                sx={{
                  alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                  bgcolor: msg.role === "user" ? "#1976d2" : "#fff",
                  color: msg.role === "user" ? "#fff" : "#000",
                  px: 2,
                  py: 1,
                  borderRadius: 2,
                  maxWidth: "80%",
                  whiteSpace: "pre-line",
                }}
              >
                {msg.content}
              </Box>
            ))}
          </Box>

          <Divider />
          <Box
            component="form"
            onSubmit={(e) => {
              e.preventDefault();
              handleChat();
            }}
            sx={{
              p: 2,
              borderTop: "1px solid #ddd",
              display: "flex",
              alignItems: "center",
              backgroundColor: "#fff",
            }}
          >
            <TextField
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Write a message"
              variant="outlined"
              size="small"
              fullWidth
              sx={{ mr: 1 }}
            />
            <IconButton type="submit" color="primary">
              <SendIcon />
            </IconButton>
          </Box>
        </Paper>
      )}
    </>
  );
}
