'use client';

import { useState } from 'react';

export default function AIBot({ setPlanningSummary, setChartData }) {
  const [inputText, setInputText] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleChat = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/chatbot/response', { //백엔드의 Chatbot API 호출 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          input: inputText,
          history: chatHistory.map(({ user, bot }) => [user, bot]), 
        }),
      });

      if (!res.ok) throw new Error('API 응답 오류');
      const data = await res.json();

      // 상위 컴포넌트에 수집된 변수 전달
      console.log(data)
      if (
        data.analysis_results &&
        data.analysis_results.accumulated_sales_planning &&
        typeof setChartData === 'function'
      ) {
        setChartData(data.analysis_results.accumulated_sales_planning.predictions);
      }

      // chat_history가 [[user, bot], ...]이면 변환
      if (Array.isArray(data.chat_history)) {
        const converted = data.chat_history.map(([user, bot]) => ({
          user,
          bot,
        }));
        setChatHistory(converted);
      } else {
        // 없을 경우 수동으로 한 쌍 추가
        setChatHistory((prev) => [
          ...prev,
          { user: inputText, bot: data.response_text || '응답 없음' },
        ]);
      }

      setInputText('');
    } catch (error) {
      console.error('채팅 요청 실패: ', error);
    }
  };

  return (
    <div className="bg-gray-50 p-4 rounded border border-gray-200 shadow-sm">
      <h3 className="font-semibold mb-2 text-lg">AI 기획 챗봇</h3>
      <p className="text-sm text-gray-600 mb-4">
        공연 기획 챗봇과 이야기를 나눠봐요!
      </p>

      {/* 대화 출력 영역 */}
      {chatHistory.length > 0 && (
        <div className="mb-4 max-h-72 overflow-y-auto pr-2">
          {chatHistory.map((chat, idx) => (
            <div key={idx} className="mb-3">
              {chat.user && (
                <p className="text-sm text-gray-800">
                  <strong>사용자:</strong> {chat.user}
                </p>
              )}
              {chat.bot && (
                <p className="text-sm text-gray-800">
                  <strong>챗봇:</strong> {chat.bot}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* 입력창 */}
      <div className="flex">
        <input
          type="text"
          value={inputText}
          placeholder="공연 기획에 대해 입력..."
          onChange={(e) => setInputText(e.target.value)}
          className="flex-grow border border-gray-300 rounded p-2 mr-2 text-sm"
        />
        <button
          onClick={handleChat}
          className="px-4 py-2 bg-green-500 text-white rounded text-sm hover:bg-green-600 transition"
        >
          전송
        </button>
      </div>
    </div>
  );
}
