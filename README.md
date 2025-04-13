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