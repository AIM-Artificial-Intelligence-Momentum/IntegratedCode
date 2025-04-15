//scenes/chatg/index.jsx
"use client";

import { useState } from "react";
import {
  Box,
  IconButton,
  TextField,
  Paper,
  Typography,
  Divider
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import ChatIcon from "@mui/icons-material/Chat";
import CloseIcon from "@mui/icons-material/Close";

export default function ChatPage({ onUpdateInsights }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "안녕하세요!\n\n예산, 장르, 지역 등 다양한 요소에 대해 질문드릴게요. 자유롭게 말씀해주세요.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");

    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: updatedMessages }),
    });

    const data = await res.json();
    const reply = data.reply;
    setMessages((prev) => [...prev, { role: "assistant", content: reply }]);

    // ⬇️ 인사이트 업데이트 트리거
    if (onUpdateInsights && typeof data.insights === "object") {
      onUpdateInsights(data.insights);
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
            '&:hover': { bgcolor: "primary.dark" }
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
            {messages.map((msg, idx) => (
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
              handleSend();
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
              value={input}
              onChange={(e) => setInput(e.target.value)}
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
