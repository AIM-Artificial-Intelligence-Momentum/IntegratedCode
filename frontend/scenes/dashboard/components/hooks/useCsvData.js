// scenes/dashboard/hooks/useCsvData.js
import { useEffect, useState } from "react";

export default function useCsvData() {
  const [scenarioData, setScenarioData] = useState({});

  useEffect(() => {
    const loadJson = async () => {
      const [audienceRes, performanceRes, salesRes] = await Promise.all([
        fetch("/audience_tb.json"),
        fetch("/performance_tb.json"),
        fetch("/sales_tb.json"),
      ]);

      const [audience, performance, sales] = await Promise.all([
        audienceRes.json(),
        performanceRes.json(),
        salesRes.json(),
      ]);

      setScenarioData({
        "관객 수 예측 – 기획 단계": [
          {
            chartType: "bar",
            title: "동일 장르 내 과거 공연 관객 수 비교",
            xField: "performance_name",
            yFields: ["actual", "predicted"],
            data: performance,
          },
          {
            chartType: "scatter",
            title: "좌석 수 대비 예측 관객 수",
            xField: "capacity",
            yField: "predicted_sales",
            categoryField: "genre",
            data: performance,
          },
          {
            chartType: "multi-line",
            title: "예측 관객 추이 시계열",
            xField: "date",
            yFields: ["뮤지컬 캣츠", "콘서트 아이유"],
            data: [
              { date: "2025-05-01", "뮤지컬 캣츠": 100, "콘서트 아이유": 200 },
              { date: "2025-05-02", "뮤지컬 캣츠": 250, "콘서트 아이유": 500 },
              { date: "2025-05-03", "뮤지컬 캣츠": 400, "콘서트 아이유": 800 },
            ],
          },
        ],
        "관객 수 예측 – 판매 단계": [
          {
            chartType: "line",
            title: "일별 판매량 추이",
            xField: "date",
            yField: "daily_sales",
            data: sales,
          },
        ],
        "티켓 판매 위험 예측 – 판매 단계 조기 경보": [
          {
            chartType: "table",
            title: "과거 공연 리스트 테이블",
            columns: ["performance_name", "actual_booking_rate", "predicted_risk"],
            data: performance,
          },
          {
            chartType: "roc-curve",
            title: "ROC 및 PR Curve",
            xField: "fpr",
            yField: "tpr",
            data: [
              { fpr: 0.0, tpr: 0.0 },
              { fpr: 0.1, tpr: 0.5 },
              { fpr: 0.2, tpr: 0.75 },
              { fpr: 0.3, tpr: 0.85 },
              { fpr: 0.4, tpr: 0.9 },
              { fpr: 0.5, tpr: 0.93 },
              { fpr: 0.6, tpr: 0.95 },
              { fpr: 0.7, tpr: 0.96 },
              { fpr: 0.8, tpr: 0.98 },
              { fpr: 0.9, tpr: 0.99 },
              { fpr: 1.0, tpr: 1.0 },
            ],
          },
          {
            chartType: "line",
            title: "예매 추이 비교 그래프",
            xField: "date",
            yFields: ["booking_rate", "target_booking_rate"],
            data: [
              { date: "2025-08-01", booking_rate: 50, target_booking_rate: 75 },
              { date: "2025-08-02", booking_rate: 55, target_booking_rate: 75 },
              { date: "2025-08-03", booking_rate: 58, target_booking_rate: 75 },
              { date: "2025-08-04", booking_rate: 62, target_booking_rate: 75 },
              { date: "2025-08-05", booking_rate: 68, target_booking_rate: 75 },
              { date: "2025-08-06", booking_rate: 72, target_booking_rate: 75 },
              { date: "2025-08-07", booking_rate: 76, target_booking_rate: 75 },
            ],
          },
        ],
        "집계 시각화": [
          {
            chartType: "bar",
            title: "지역별 예약 수",
            xField: "region",
            yField: "booking_count",
            data: audience,
          },
        ],
      });
    };

    loadJson();
  }, []);

  return scenarioData;
}
