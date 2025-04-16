//scenes/dashboard/index.jsx
"use client";

import { useState, useRef } from "react";
import { Box, Typography, Button, Paper } from "@mui/material";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import ChatPage from "../chat/index";
import dynamic from "next/dynamic";

const InsightChart = dynamic(() => import("./components/InsightChart"), { ssr: false });

const Dashboard = () => {
  const [insightDataFromChatGpt, setInsightDataFromChatGpt] = useState([]);
  const insightRef = useRef();

  const handleDownloadPDF = async () => {
    if (!insightRef.current) return;

    const canvas = await html2canvas(insightRef.current);
    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save("insight-report.pdf");
  };

  return (
    <Box m="10px">
      {/* ChatGPT 연결 */}
      <ChatPage onUpdateInsights={setInsightDataFromChatGpt} />

      {/* PDF 다운로드 버튼 */}
      <Box display="flex" justifyContent="flex-end" alignItems="center" my={2}>
        <Button
          onClick={handleDownloadPDF}
          sx={{ fontSize: "14px", fontWeight: "bold", padding: "10px 20px" }}
        >
          <DownloadOutlinedIcon sx={{ mr: "10px" }} />
          Download Reports
        </Button>
      </Box>

      {/* 인사이트 영역 (PDF 대상) */}
      <Paper ref={insightRef} elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" fontWeight="bold" mb={3}>
          Insight Report
        </Typography>
        <InsightChart externalData={insightDataFromChatGpt} />
      </Paper>
    </Box>
  );
};

export default Dashboard;