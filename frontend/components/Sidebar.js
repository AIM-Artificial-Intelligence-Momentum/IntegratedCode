// components/Sidebar.js
'use client';

import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import AIBot from './AIBot';

export default function Sidebar({ planningSummary, setPlannningSummary, setChartData}) {
    const exportPDF = async () => {
        const input = document.getElementById('dashboard');
        if (!input) return;
        try {
            const canvas = await html2canvas(input, { scale: 2 });
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jsPDF('p', 'mm', 'a4');
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
            pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
            pdf.save('dashboard.pdf');
        } catch (err) {
            console.error('PDF 생성 중 오류: ', err);
        }
    };

    return (
        <div className='w-full md:w-full lg:w-full p-4 border-r border-gray-200 flex flex-col justify-between bg-white'>
            <div>
                <h2 className='text-xl font-bold mb-4'>공연 기획 요약</h2>
                <p><strong>공연명:</strong> {planningSummary.showName}</p>
                <p><strong>공연 기간:</strong> {planningSummary.showPeriod}</p>
                <p><strong>개최 장소:</strong> {planningSummary.location}</p>
                <p><strong>목표 관객 수:</strong> {planningSummary.targetAudience}명</p>
                <p><strong>예상 매출:</strong> {planningSummary.predictedRevenue}원</p>
                <p><strong>소요 예산:</strong> {planningSummary.estimatedCost}원</p>
                <p><strong>출연진:</strong> {planningSummary.performers}</p>

                <button
                    onClick={exportPDF}
                    className='mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition'
                >
                    PDF로 보내기
                </button>
            </div>
            <div className='mt-4'>
                <AIBot setPlanningSummary={setPlannningSummary} setChartData={setChartData}/>
            </div>
        </div>
        

    );
}