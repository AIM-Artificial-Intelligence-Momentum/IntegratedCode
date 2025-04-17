/// scenes/dashboard/components/InsightCharts.jsx
'use client';

import { useEffect, useRef, useState } from "react";
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Divider,
} from "@mui/material";
import { renderCharts } from "./chartHelpers";
import useCsvData from "./hooks/useCsvData";
import useCsvObserver from "./utils/useCsvObserver";

export default function InsightChart({ onTabChange, externalData, externalStructredData, realInsightFromChatGpt, aisearchFromChatGpt}) {
  const dataBySection = useCsvData();
  const scenarioTitles = Object.keys(dataBySection);
  const [activeTab, setActiveTab] = useState(0);
  const sectionRefs = useRef([]);

  // const [activeChartData, setActiveChartData] = useState([]);
  const [structuredInfo, setStructuredInfo] = useState(null);
  const [realChartData, setRealChartData] = useState(null);
  const [aiSearchSummary, setAISearchSummary] = useState(null);

  // useEffect(() => {
  //   if (externalData && externalData.length > 0) {
  //     setActiveChartData(externalData);
  //   }
  // }, [externalData]);

  useEffect(() => {
    if (externalStructredData && Object.keys(externalStructredData).length > 0) {
      setStructuredInfo(externalStructredData);
    }
  }, [externalStructredData]);

  useEffect(() => {
    if (realInsightFromChatGpt && Object.keys(realInsightFromChatGpt).length > 0) {
      setRealChartData(realInsightFromChatGpt);
    }
  }, [realInsightFromChatGpt]);

  useEffect(() => {
    if (aisearchFromChatGpt && Object.keys(aisearchFromChatGpt).length > 0) {
      setAISearchSummary(aisearchFromChatGpt);
    }
  }, [aisearchFromChatGpt]);

  // 탭 추가(Structured Insights,Real Insights) 
  const extraTabs = [];
  if (structuredInfo) extraTabs.push("🤖 GPT가 수집한 변수");
  // if (realChartData) extraTabs.push("🖥️ 인사이트 정리");
  if (aiSearchSummary) extraTabs.push("📖 관련 문서 요약")
  const allTabs = [...scenarioTitles, ...extraTabs];

  const handleTabClick = (index) => {
    const targetRef = sectionRefs.current[index];
    if (targetRef) {
      targetRef.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };
  const salesStageKeyMap = {
    genre: "장르",
    region: "지역",
    start_date: "공연 시작일",
    capacity: "좌석 수",
    star_power: "출연진 인기",
    ticket_price: "티켓 가격",
    marketing_budget: "마케팅 예산",
    sns_mention_count: "SNS 언급량",
    daily_sales: "일일 판매량",
    booking_rate: "예매율",
    ad_exposure: "광고 노출",
    production_cost: "제작비",
    variable_cost_rate: "변동비 비율",
    accumulated_sales: "누적 판매량",
    sns_mention_daily: "SNS 일일 언급량",
    promo_event_flag: "프로모션 이벤트 여부",
    duration: "공연 기간"
  };
  
  function translateKeyToKorean(key) {
    return salesStageKeyMap[key] || key;
  }

  useCsvObserver(sectionRefs, dataBySection, setActiveTab, onTabChange);

  return (
    <Box>
      <Box sx={{ position: "sticky", top: 0, zIndex: 10, backgroundColor: "#fff", py: 1 }}>
        <Tabs
          value={activeTab}
          onChange={(e, newVal) => handleTabClick(newVal)}
          variant="scrollable"
          scrollButtons="auto"
        >
          {allTabs.map((title, idx) => (
            <Tab key={idx} label={title} />
          ))}
        </Tabs>
      </Box>

      {allTabs.map((title, idx) => {
        const isStructured = title === "🤖 GPT가 수집한 변수";
        const isReal = title === "🖥️ 인사이트 정리";
        const isAISearch = title === "📖 관련 문서 요약";

        return (
          <Box
            key={idx}
            ref={(el) => (sectionRefs.current[idx] = el)}
            sx={{ scrollMarginTop: "60px", mb: 6 }}
          >
            <Typography variant="h6" fontWeight="bold" mb={2}>
              {title}
            </Typography>

            {isStructured ? (
              Object.entries(structuredInfo).map(([key, value]) => (
                <Typography key={key} variant="body1" sx={{ mb: 1, fontSize: "1.25rem" }}>
                  <strong>{translateKeyToKorean(key)}</strong>: {String(value)}
                </Typography>
              ))
            ) : 
            isAISearch ? (
              <Box
                component="pre"
                sx={{
                  backgroundColor: "#f0f9ff",
                  p: 2,
                  borderRadius: 2,
                  overflowX: "auto",
                  fontFamily: "monospace",
                  whiteSpace: "pre-wrap",
                }}
              >
                {aiSearchSummary
                  .replace(/\\n/g, "\n")            // \n → 실제 줄바꿈
                  .split("\n\n")                    // 문단 기준 분리
                  .map((para, idx) => (
                    <Typography
                      key={idx}
                      variant="body1"
                      sx={{ mb: 2, whiteSpace: "pre-wrap", fontFamily: "inherit" }}
                    >
                      {para}
                    </Typography>
                  ))}
              </Box>
            ) : (
              renderCharts(dataBySection[title])
            )}

            <Divider sx={{ my: 4 }} />
          </Box>
        );
      })}
    </Box>
  );
}