# PERFORMANCE_PLANNING

Next.js 13 App Router 기반 공연 기획 대시보드 예시

## 주요 기능

- 좌측: 공연 기획 요약, AI 기획 챗봇, PDF 내보내기
- 우측: D3.js 데이터 시각화 (라인, 파이, 바 차트)
- Tailwind CSS 스타일
- html2canvas + jsPDF로 PDF 내보내기

## 실행 방법

```bash
npm install
npm run dev
```

## 챗봇 API(/api/chatbot/response) 

- api/chatbot/response 경로의 라우터입니다. 
- 함수인자값 : Request 요청(body에 user_input과 history가 담겨있어야 합니다.)
```bash
@router.post("/response")
async def respond(request: Request):
    body = await request.json()
    user_input = body.get("input", "")
    history = body.get("history", [])

    if not user_input:
        return JSONResponse(content={"error": "입력값이 비어 있습니다."}, status_code=400)

    try:
        result = await chatbot_service.handle_user_input(user_input, history)
        return JSONResponse(content=result)
```
- 프론트엔드에서 접근할 수 있는 형식 및 리턴값 
 response.data.chat_history : 전체 사용자, 챗봇 히스토리 출력 
 response.data.structured_data : 챗봇 응답만 출력
 response.data.response_text : 현재까지 모인 JSON 변수
 response.data.intent : 사용자 의도 분류(수집 / 검색 / 혼합)
 response.data.stage : 사용자가 있는 공연 단계(기획 / 판매)
