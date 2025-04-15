import { Chart as ChartJS, CategoryScale,LinearScale, BarElement,PointElement,LineElement,Tooltip,Legend,} from 'chart.js';
import { Bar,Line,} from 'react-chartjs-2';
// 둘다 npm 자체 패키지 
  
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Tooltip,
    Legend
);
  
export default function ChartVisualizer({ data }) {
    const capacityData = {
        labels: data.capacity_scatter.data.map((d) => d.capacity + '석'),
        datasets: [{
        label: '예측 관객 수',
        data: data.capacity_scatter.data.map((d) => d.predicted_sales), // 예측 관객 수 
        backgroundColor: '#3b82f6'
        }]
    };
  
    const comparisonData = {
      labels: data.comparison.performances.map((p) => p.performance_name),
      datasets: [
        {
          label: '실제 관객',
          data: data.comparison.performances.map((p) => p.actual), //실제 관객과 예측 관객 비교 
          backgroundColor: '#e5e7eb',
        },
        {
          label: '예측 관객',
          data: data.comparison.performances.map((p) => p.predicted),
          backgroundColor: '#10b981',
        }
      ]
    };
  
    const timeSeriesData = {
      labels: data.time_series.dates,
      datasets: [{
        label: '누적 관객 수',
        data: data.time_series.predicted_cumulative, // 누적 관객 수
        borderColor: '#6366f1',
        fill: false
      }]
    };
  
    return (
      <div className="mt-6 space-y-6">
        <div>
          <h4 className="text-sm font-semibold mb-2">공연장 수용 규모에 따른 예측 관객 수</h4>
          <Bar data={capacityData} />
        </div>
        <div>
          <h4 className="text-sm font-semibold mb-2">유사 공연과 비교한 실제 관객과 예측 관객 수</h4>
          <Bar data={comparisonData} />
        </div>
        <div>
          <h4 className="text-sm font-semibold mb-2">예측 누적 관객 추이</h4>
          <Line data={timeSeriesData} />
        </div>
      </div>
    );
  }
  