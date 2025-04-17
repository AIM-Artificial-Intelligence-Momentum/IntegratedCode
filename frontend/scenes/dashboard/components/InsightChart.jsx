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

export default function InsightChart({ onTabChange, externalData, externalStructredData, realInsightFromChatGpt}) {
  const dataBySection = useCsvData();
  const scenarioTitles = Object.keys(dataBySection);
  const [activeTab, setActiveTab] = useState(0);
  const sectionRefs = useRef([]);

  // const [activeChartData, setActiveChartData] = useState([]);
  const [structuredInfo, setStructuredInfo] = useState(null);
  const [realChartData, setRealChartData] = useState(null);

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

  // 탭 추가(Structured Insights,Real Insights) 
  const extraTabs = [];
  if (structuredInfo) extraTabs.push("📘 Structured Insights");
  if (realChartData) extraTabs.push("💃 Real Insights");
  const allTabs = [...scenarioTitles, ...extraTabs];

  const handleTabClick = (index) => {
    const targetRef = sectionRefs.current[index];
    if (targetRef) {
      targetRef.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

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
        const isStructured = title === "📘 Structured Insights";
        const isReal = title === "💃 Real Insights";

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
                <Typography key={key} variant="body1" sx={{ mb: 1 }}>
                  <strong>{key}</strong>: {String(value)}
                </Typography>
              ))
            ) : isReal ? (
              <Box
                component="pre"
                sx={{
                  backgroundColor: "#f5f5f5",
                  p: 2,
                  borderRadius: 2,
                  overflowX: "auto",
                  fontFamily: "monospace",
                  whiteSpace: "pre-wrap",
                }}
              >
                {JSON.stringify(realChartData, null, 2)}
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