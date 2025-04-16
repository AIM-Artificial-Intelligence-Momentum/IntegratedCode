/// scenes/dashboard/components/InsightCharts.jsx
'use client';

import { useRef, useState } from "react";
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

export default function InsightChart({ onTabChange }) {
  const dataBySection = useCsvData(); // 시나리오별 데이터
  const scenarioTitles = Object.keys(dataBySection); // 동적 탭 생성
  const [activeTab, setActiveTab] = useState(0);
  const sectionRefs = useRef([]);

  const handleTabClick = (index) => {
    const targetRef = sectionRefs.current[index];
    if (targetRef) {
      targetRef.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  // 스크롤 감지 → activeTab 업데이트
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
          {scenarioTitles.map((title, idx) => (
            <Tab key={idx} label={title} />
          ))}
        </Tabs>
      </Box>

      {scenarioTitles.map((title, idx) => (
        <Box
          key={idx}
          ref={(el) => (sectionRefs.current[idx] = el)}
          sx={{ scrollMarginTop: "60px", mb: 6 }}
        >
          <Typography variant="h6" fontWeight="bold" mb={2}>
            {title}
          </Typography>
          {renderCharts(dataBySection[title])}
          <Divider sx={{ my: 4 }} />
        </Box>
      ))}
    </Box>
  );
}
