// src/app/page.js
'use client';

import { useState } from 'react';
import Sidebar from '../../components/Sidebar';
import Charts from '../../components/Charts';

export default function Home() {
  const [planningSummary, setPlanningSummary] = useState({
    showName: '해설이 있는 음악회',
    showPeriod: '2021-01-01 ~ 2021-12-31',
    location: 'OO예술의 전당',
    targetAudience: 4000,
    predictedRevenue: 60000000,
    estimatedCost: 30000000,
    performers: '00 오케스트라 / 00 무용단',
    audienceTrend: [4000, 4200, 4500, 4700, 4900],
    marketingBreakdown: [
      { category: '온라인 홍보', value: 25 },
      { category: '지역문화홍보', value: 15 },
      { category: '기타 마케팅', value: 10 },
    ],
  });

  return (
    <div id="dashboard" className="flex flex-col md:flex-row h-screen">
      {/* 작은 화면: 세로 배치, md 이상: 좌측 1/3, 우측 2/3 */}
      <div className="md:w-1/3">
        <Sidebar planningSummary={planningSummary} setPlanningSummary={setPlanningSummary} />
      </div>
      <div className="md:w-2/3">
        <Charts planningSummary={planningSummary} />
      </div>
    </div>
  );
}
