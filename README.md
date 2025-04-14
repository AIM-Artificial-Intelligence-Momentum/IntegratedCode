이 링크 타고 들어가시면 프로젝트 구조에 대한 자세한 설명과 실행 방법이 있습니다.

https://curly-cookie-e4a.notion.site/2-Project-1ce4fa74154b80c4bedbd1cdc40bde25

#2025_4_7 : 챗봇 기능 구현
![image](https://github.com/user-attachments/assets/912a38a1-b2db-4855-ab36-5a5f48974b57)

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

## Project Tree

```
IntegratedCode
├─ backend
│  ├─ AzureServiceModule
│  │  ├─ AzureAISearch.py
│  │  ├─ AzureCLUClient.py
│  │  ├─ AzureOpenAIChat.py
│  │  ├─ backup
│  │  │  └─ AzureOpenAIChat.py
│  │  ├─ ServiceRouter.py
│  │  ├─ test2.py
│  │  └─ test_aisearch.py
│  ├─ demo.py
│  ├─ ModelPredictionModule
│  │  ├─ analysis_module.py
│  │  ├─ json_requests_test.py
│  │  ├─ models
│  │  │  ├─ kmeans_audience_seg.pkl
│  │  │  ├─ rf_cls_ticket_risk.pkl
│  │  │  ├─ xgb_reg_accumulated_sales_planning.pkl
│  │  │  ├─ xgb_reg_accumulated_sales_selling.pkl
│  │  │  ├─ xgb_reg_roi_bep_planning.pkl
│  │  │  └─ xgb_reg_roi_bep_selling.pkl
│  │  ├─ test_analysis.py
│  │  └─ ticket_risk_roc_pr.py
│  ├─ requirements.txt
│  └─ routes
│     ├─ AISearchAPI.py
│     ├─ CLUAnalysisAPI.py
│     └─ MLAnalysisAPI.py
├─ backup
│  └─ README.md
├─ components
│  ├─ AIBot.js
│  ├─ ChartBar.js
│  ├─ ChartLine.js
│  ├─ ChartPie.js
│  ├─ Charts.js
│  └─ Sidebar.js
├─ demo.py
├─ eslint.config.mjs
├─ frontend
│  ├─ .next
│  │  ├─ app-build-manifest.json
│  │  ├─ build-manifest.json
│  │  ├─ cache
│  │  │  ├─ .rscinfo
│  │  │  └─ webpack
│  │  │     ├─ client-development
│  │  │     │  ├─ 0.pack.gz
│  │  │     │  ├─ 1.pack.gz
│  │  │     │  ├─ index.pack.gz
│  │  │     │  └─ index.pack.gz.old
│  │  │     └─ server-development
│  │  │        ├─ 0.pack.gz
│  │  │        ├─ 1.pack.gz
│  │  │        ├─ index.pack.gz
│  │  │        └─ index.pack.gz.old
│  │  ├─ package.json
│  │  ├─ react-loadable-manifest.json
│  │  ├─ server
│  │  │  ├─ app
│  │  │  │  ├─ favicon.ico
│  │  │  │  │  └─ route.js
│  │  │  │  ├─ page.js
│  │  │  │  └─ page_client-reference-manifest.js
│  │  │  ├─ app-paths-manifest.json
│  │  │  ├─ interception-route-rewrite-manifest.js
│  │  │  ├─ middleware-build-manifest.js
│  │  │  ├─ middleware-manifest.json
│  │  │  ├─ middleware-react-loadable-manifest.js
│  │  │  ├─ next-font-manifest.js
│  │  │  ├─ next-font-manifest.json
│  │  │  ├─ pages-manifest.json
│  │  │  ├─ server-reference-manifest.js
│  │  │  ├─ server-reference-manifest.json
│  │  │  ├─ vendor-chunks
│  │  │  │  ├─ @babel.js
│  │  │  │  ├─ @swc.js
│  │  │  │  ├─ canvg.js
│  │  │  │  ├─ core-js.js
│  │  │  │  ├─ d3-array.js
│  │  │  │  ├─ d3-axis.js
│  │  │  │  ├─ d3-brush.js
│  │  │  │  ├─ d3-chord.js
│  │  │  │  ├─ d3-color.js
│  │  │  │  ├─ d3-contour.js
│  │  │  │  ├─ d3-delaunay.js
│  │  │  │  ├─ d3-dispatch.js
│  │  │  │  ├─ d3-drag.js
│  │  │  │  ├─ d3-dsv.js
│  │  │  │  ├─ d3-ease.js
│  │  │  │  ├─ d3-fetch.js
│  │  │  │  ├─ d3-force.js
│  │  │  │  ├─ d3-format.js
│  │  │  │  ├─ d3-geo.js
│  │  │  │  ├─ d3-hierarchy.js
│  │  │  │  ├─ d3-interpolate.js
│  │  │  │  ├─ d3-path.js
│  │  │  │  ├─ d3-polygon.js
│  │  │  │  ├─ d3-quadtree.js
│  │  │  │  ├─ d3-random.js
│  │  │  │  ├─ d3-scale-chromatic.js
│  │  │  │  ├─ d3-scale.js
│  │  │  │  ├─ d3-selection.js
│  │  │  │  ├─ d3-shape.js
│  │  │  │  ├─ d3-time-format.js
│  │  │  │  ├─ d3-time.js
│  │  │  │  ├─ d3-timer.js
│  │  │  │  ├─ d3-transition.js
│  │  │  │  ├─ d3-zoom.js
│  │  │  │  ├─ d3.js
│  │  │  │  ├─ delaunator.js
│  │  │  │  ├─ dompurify.js
│  │  │  │  ├─ fflate.js
│  │  │  │  ├─ html2canvas.js
│  │  │  │  ├─ internmap.js
│  │  │  │  ├─ jspdf.js
│  │  │  │  ├─ next.js
│  │  │  │  ├─ performance-now.js
│  │  │  │  ├─ raf.js
│  │  │  │  ├─ rgbcolor.js
│  │  │  │  ├─ robust-predicates.js
│  │  │  │  ├─ stackblur-canvas.js
│  │  │  │  └─ svg-pathdata.js
│  │  │  └─ webpack-runtime.js
│  │  ├─ static
│  │  │  ├─ chunks
│  │  │  │  ├─ app
│  │  │  │  │  ├─ layout.js
│  │  │  │  │  └─ page.js
│  │  │  │  ├─ app-pages-internals.js
│  │  │  │  ├─ main-app.js
│  │  │  │  ├─ polyfills.js
│  │  │  │  └─ webpack.js
│  │  │  ├─ css
│  │  │  │  └─ app
│  │  │  │     └─ layout.css
│  │  │  ├─ development
│  │  │  │  ├─ _buildManifest.js
│  │  │  │  └─ _ssgManifest.js
│  │  │  ├─ media
│  │  │  │  ├─ 569ce4b8f30dc480-s.p.woff2
│  │  │  │  ├─ 747892c23ea88013-s.woff2
│  │  │  │  ├─ 93f479601ee12b01-s.p.woff2
│  │  │  │  └─ ba015fad6dcf6784-s.woff2
│  │  │  └─ webpack
│  │  │     └─ 633457081244afec._.hot-update.json
│  │  ├─ trace
│  │  └─ types
│  │     ├─ app
│  │     │  ├─ layout.ts
│  │     │  └─ page.ts
│  │     ├─ cache-life.d.ts
│  │     └─ package.json
│  ├─ components
│  │  ├─ AIBot.js
│  │  ├─ ChartBar.js
│  │  ├─ ChartLine.js
│  │  ├─ ChartPie.js
│  │  ├─ Charts.js
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
├─ jsconfig.json
├─ next.config.mjs
├─ package-lock.json
├─ package.json
├─ postcss.config.mjs
├─ public
│  ├─ file.svg
│  ├─ globe.svg
│  ├─ next.svg
│  ├─ vercel.svg
│  └─ window.svg
├─ README.md
├─ requirements.txt
├─ routes
│  ├─ CLUAnalysisAPI.py
│  └─ MLAnalysisAPI.py
└─ src
   └─ app
      ├─ api
      │  └─ chat
      │     └─ route.js
      ├─ favicon.ico
      ├─ globals.css
      ├─ layout.js
      └─ page.js

```
