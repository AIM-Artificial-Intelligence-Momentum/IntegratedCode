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

export default function InsightChart({ onTabChange, externalData }) {
  const dataBySection = useCsvData();
  const scenarioTitles = Object.keys(dataBySection);
  const [activeTab, setActiveTab] = useState(0);
  const sectionRefs = useRef([]);
  const [activeChartData, setActiveChartData] = useState([]);

  useEffect(() => {
    if (externalData && externalData.length > 0) {
      setActiveChartData(externalData);
    }
  }, [externalData]);

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

      {activeChartData && activeChartData.length > 0 && (
        <Box mt={6}>
          <Typography variant="h6" fontWeight="bold" mb={2}>
            🧠 ChatGPT Generated Insights
          </Typography>
          {renderCharts(activeChartData)}
        </Box>
      )}
    </Box>
  );
}