// components/Charts.js
'use client';

import ChartLine from './ChartLine';
import ChartPie from './ChartPie';
import ChartBar from './ChartBar';

export default function Charts({ planningSummary }) {
  return (
    <div className="flex-1 p-4 overflow-auto">
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2">관객 증감 추이 (라인 차트)</h3>
        <div className="bg-white p-4 rounded border border-gray-200">
          <ChartLine data={planningSummary.audienceTrend} />
        </div>
      </div>
      <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded border border-gray-200">
          <h3 className="text-md font-semibold mb-2">마케팅 예산 분포 (파이 차트)</h3>
          <ChartPie data={planningSummary.marketingBreakdown} />
        </div>
        <div className="bg-white p-4 rounded border border-gray-200">
          <h3 className="text-md font-semibold mb-2">티켓 유형 분포 (파이 차트)</h3>
          <ChartPie data={planningSummary.marketingBreakdown} />
        </div>
      </div>
      <div className="mb-8">
        <h3 className="text-md font-semibold mb-2">마케팅 채널 예산 분석 (바 차트)</h3>
        <div className="bg-white p-4 rounded border border-gray-200">
          <ChartBar data={planningSummary.marketingBreakdown} />
        </div>
      </div>
    </div>
  );
}
