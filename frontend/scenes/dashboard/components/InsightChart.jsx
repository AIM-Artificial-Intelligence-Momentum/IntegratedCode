// scenes/dashboard/components/InsightChart.jsx
import { useEffect, useState } from "react";
import Papa from "papaparse";
import { Box, Typography, Grid } from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#ff8042"];

export default function InsightChart({ externalData }) {
  const [mergedData, setMergedData] = useState([]);

  useEffect(() => {
    const loadMultipleCsvs = async () => {
      const sources = [
        "/data/audience_tb.csv",
        "/data/sales_tb.csv",
        "/data/performance_tb.csv",
      ];

      const allData = [];

      for (const path of sources) {
        const res = await fetch(path);
        const text = await res.text();
        const parsed = Papa.parse(text, { header: true });
        const cleaned = parsed.data.filter((row) => Object.values(row).some((v) => v !== ""));
        allData.push(...cleaned);
      }

      if (externalData && Array.isArray(externalData)) {
        allData.push(...externalData);
      }

      setMergedData(allData);
    };

    loadMultipleCsvs();
  }, [externalData]);

  const chartsToRender = [];

  if (mergedData.length > 0) {
    const sample = mergedData[0];
    const keys = Object.keys(sample);

    if (keys.includes("target_booking_rate")) {
      chartsToRender.push(
        <BarChart key="bar" data={mergedData}>
          <XAxis dataKey="장르" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="target_booking_rate" fill="#1976d2" />
        </BarChart>
      );
    }

    if (keys.includes("region") && keys.includes("ticket_revenue")) {
      chartsToRender.push(
        <PieChart key="pie">
          <Pie
            data={mergedData}
            dataKey="ticket_revenue"
            nameKey="region"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            label
          >
            {mergedData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      );
    }

    if (keys.includes("date") && keys.includes("predict_cumulative")) {
      chartsToRender.push(
        <LineChart key="line" data={mergedData}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="predict_cumulative" stroke="#8884d8" />
          <Line type="monotone" dataKey="actual_cumulative" stroke="#82ca9d" />
        </LineChart>
      );
    }

    if (keys.includes("ROI(predictions[0])")) {
      chartsToRender.push(
        <LineChart key="roi" data={mergedData}>
          <XAxis dataKey="공연명" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="ROI(predictions[0])" stroke="#ff8042" />
        </LineChart>
      );
    }
  }

  if (chartsToRender.length === 0) return <Typography>분석할 데이터가 없습니다.</Typography>;

  return (
    <Box>
      <Typography variant="h6" mb={2}>자동 인사이트 시각화</Typography>
      <Grid container spacing={3}>
        {chartsToRender.map((chart, idx) => (
          <Grid item xs={12} md={6} key={idx}>
            <ResponsiveContainer width="100%" height={300}>
              {chart}
            </ResponsiveContainer>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}