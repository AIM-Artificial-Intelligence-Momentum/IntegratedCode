## components/AIBot.js에서 채팅 API와 연결

![image](https://github.com/user-attachments/assets/e39aeef2-f780-405f-bb75-95ca15bce878)

## components/ChartVisualizer.js를 통해 기존 차트에 동적 차트 추가함.

![image](https://github.com/user-attachments/assets/ffbeb18c-2b94-47dd-8b81-6fda56433793)

일단 테스트용으로 화면에 표시 가능한지 확인헀습니다. 참고해서 만들어주세요!

## analysis_results가 반환하는 값

```bash
analysis_results
	accumulated_sales_planning
		predictions
			capacity_scatter
				data : Array(3)
					0 : 
					capacity: 500
					genre : "뮤지컬"
					performance_id : 101
					predicted_sales : 298.5381164550781
					1 : 
					capacity: 750 
					genre : "뮤지컬"
					performance_id : 102
					predicted_sales : 348.5381164550781
					2:
					capacity: 600 
					genre : "뮤지컬"
					performance_id : 103
					predicted_sales : 268.5381164550781
			comparison
				performances : Array(5)
					0 : 
					actual : 2800
					performance_id : 101
					performance_name : "뮤지컬 캣츠"
					predicted : 298.5381164550781
					1 : 
					actual : 3000
					performance_id : 102
					performance_name : "콘서트 아이유"
					predicted : 418.5381164550781
					2 : 
					actual : 2500
					performance_id : 103
					performance_name : "오페라 카르멘"
					predicted : 218.53811645507812
			predictions 
				0 : 298.5381164550781	
			time_series
				confidence_interval
					lower : Array(5)
						0 : 950
						1 : 1900
						2 : 278.5381164550781
						3 : 428.5381164550781
						4 : 578.5381164550781
						length : 5
					upper : Array(5)
						0 : 950
						1 : 1900
						2 : 278.5381164550781
						3 : 428.5381164550781
						4 : 578.5381164550781
						length : 5
				dates : Array(5)
					0 : "2025-05-01"
					1 : "2025-05-02"
					2 : "2025-05-03"
					3 : "2025-05-04"
					4 : "2025-05-05"
				predicted_cumulative : Array(5)
					0 : 1000
					1 : 2000
					2 : 298.5381164550781
					3 : 448.5381164550781
					4 : 598.5381164550781
```

```
IntegratedCode
├─ backend
│  ├─ AzureServiceModule
│  │  ├─ AzureSQLClient.py
│  │  ├─ ChatbotService.py
│  │  ├─ config
│  │  │  ├─ PromptConfig.py
│  │  │  ├─ VariableConfig.py
│  │  │  └─ __init__.py
│  │  └─ modules
│  │     ├─ AISearchClient.py
│  │     ├─ AzureOpenAIClient.py
│  │     ├─ IntentClassifier.py
│  │     ├─ PromptGenerator.py
│  │     ├─ StageDetector.py
│  │     └─ VariableExtractor.py
│  ├─ demo.py
│  ├─ gradio_chat.py
│  ├─ ModelPredictionModule
│  │  ├─ analysis_module.py
│  │  ├─ models
│  │  │  ├─ kmeans_audience_seg.pkl
│  │  │  ├─ rf_cls_ticket_risk.pkl
│  │  │  ├─ xgb_reg_accumulated_sales_planning.pkl
│  │  │  ├─ xgb_reg_accumulated_sales_selling.pkl
│  │  │  ├─ xgb_reg_roi_bep_planning.pkl
│  │  │  └─ xgb_reg_roi_bep_selling.pkl
│  │  ├─ test_analysis.py
│  │  ├─ test_stats.py
│  │  └─ ticket_risk_roc_pr.py
│  ├─ requirements.txt
│  └─ routes
│     ├─ ChatbotAPI.py
│     └─ MLAnalysisAPI.py
├─ frontend
│  ├─ components
│  │  ├─ AIBot.js
│  │  ├─ ChartBar.js
│  │  ├─ ChartLine.js
│  │  ├─ ChartPie.js
│  │  ├─ Charts.js
│  │  ├─ ChartVisualizer.js
│  │  └─ Sidebar.js
│  ├─ css
│  │  └─ style.css
│  ├─ eslint.config.mjs
│  ├─ index.html
│  ├─ js
│  │  ├─ chart.js
│  │  └─ chatbot.js
│  ├─ jsconfig.json
│  ├─ next.config.mjs
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ postcss.config.mjs
│  ├─ public
│  │  ├─ file.svg
│  │  ├─ globe.svg
│  │  ├─ next.svg
│  │  ├─ vercel.svg
│  │  └─ window.svg
│  └─ src
│     └─ app
│        ├─ api
│        │  └─ chat
│        │     └─ route.js
│        ├─ favicon.ico
│        ├─ globals.css
│        ├─ layout.js
│        └─ page.js
└─ README.md

```