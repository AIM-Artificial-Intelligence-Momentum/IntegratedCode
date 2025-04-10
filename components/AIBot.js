// components/AIBot.js
/* 실제 API 연동 시나리오를 반영한 AI 챗봇
(간단한 시뮬레이션 예제) */
'use client';

import { useState } from 'react';

export default function AIBot({ setPlanningSummary }) {
    const [inputText, setInputText] = useState('');
    const [chatHistory, setChatHistory] = useState([]);

    const handleChat = async () => {
        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ inputText }),
            });
            if (!res.ok) throw new Error('API 응답 오류');
            const data = await res.json();

            setChatHistory(prev => [
                ...prev,
                { user: inputText, bot: 'AI 응답으로 업데이트 되었습니다.' },
            ]);
            setPlanningSummary(data);
            setInputText('');
        } catch (error) {
            console.error('채팅 요청 실패: ', error);
        }
    };

    return (
        <div className="bg-gray-50 p-2 rounded border border-gray-200">
          <h3 className="font-semibold mb-2">AI 기획 챗봇</h3>
          <p className="text-sm text-gray-600 mb-2">실제 AI 모델 호출하여 데이터를 업데이트합니다.</p>
          <div className="flex">
            <input
              type="text"
              value={inputText}
              placeholder="공연 기획에 대해 입력..."
              onChange={(e) => setInputText(e.target.value)}
              className="flex-grow border border-gray-300 rounded p-1 mr-2 text-sm"
            />
            <button
              onClick={handleChat}
              className="px-2 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600 transition"
            >
              전송
            </button>
          </div>
          {chatHistory.map((chat, idx) => (
            <div key={idx} className="mt-2">
              <p className="text-xs text-gray-800"><strong>사용자:</strong> {chat.user}</p>
              <p className="text-xs text-blue-600"><strong>챗봇:</strong> {chat.bot}</p>
            </div>
          ))}
        </div>
    );
}