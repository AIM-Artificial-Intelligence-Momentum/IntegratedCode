<<<<<<< HEAD
이 링크 타고 들어가시면 프로젝트 구조에 대한 자세한 설명과 실행 방법이 있습니다.

https://curly-cookie-e4a.notion.site/2-Project-1ce4fa74154b80c4bedbd1cdc40bde25

#2025_4_7 : 챗봇 기능 구현
![image](https://github.com/user-attachments/assets/912a38a1-b2db-4855-ab36-5a5f48974b57)

```
IntegratedCode
├─ backend
│  ├─ AzureServiceModule
│  │  ├─ AzureCLUClient.py
│  │  ├─ AzureOpenAIChat.py
│  │  ├─ backup
│  │  │  └─ AzureOpenAIChat.py
│  │  └─ ServiceRouter.py
│  └─ ModelPredictionModule
│     ├─ analysis_module.py
│     ├─ json_requests_test.py
│     ├─ models
│     │  ├─ kmeans_audience_seg.pkl
│     │  ├─ rf_cls_ticket_risk.pkl
│     │  ├─ xgb_reg_accumulated_sales_planning.pkl
│     │  ├─ xgb_reg_accumulated_sales_selling.pkl
│     │  ├─ xgb_reg_roi_bep_planning.pkl
│     │  └─ xgb_reg_roi_bep_selling.pkl
│     ├─ test_analysis.py
│     └─ ticket_risk_roc_pr.py
├─ demo.py
├─ frontend
│  ├─ css
│  │  └─ style.css
│  ├─ index.html
│  └─ js
│     ├─ chart.js
│     └─ chatbot.js
├─ README.md
├─ requirements.txt
└─ routes
   ├─ CLUAnalysisAPI.py
   └─ MLAnalysisAPI.py

```
=======
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

## AISearch 연동 및 API 구축
https://curly-cookie-e4a.notion.site/2-Project-1d14fa74154b80308403e8f09e14156b
>>>>>>> origin/main
