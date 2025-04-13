import { NextResponse } from 'next/server';
import axios from 'axios';

export async function Post(req) {
    try {
        const { inputText } = await req.json();

        // .env.local에서 API 설정
        const azureEndPoint = process.env.Azure_OPENAI_ENDPOINT;
        const apiKey = process.env.Azure_OPENAI_API_KEY;

        const payload = {
            prompt: inputText,
            max_token: 150,
            temporature:0.7,
        };

        // 실제 Azure OpenAI 호출(ENDPOINT 및 API 키는 환경변수로 관리)
        const response = await axios.post(azureEndPoint, payload, {
            header: {
                'Content-Type': 'application/json',
                'api-key': apiKey,
            },
        });

        // 응답 파싱(실제 API 응답 형식에 따라 수정)
        // 아래는 예시데이터, 실제 AI 응답을 원하는 데이터 형식으로 가공
        const planningSummary = {
            showName: response.data.choices?.[0]?.text?.match(/공연명:\s*(.*)/)?.[1] || "해설이 있는 음악회",
            showPeriod: "2021-01-01 ~ 2021-12-31",
            location: "OO예술의 전당",
            targetAudience: 4000,
            predicteßdRevenue: '6,000만원',
            estimatedCost: '3,000만원',
            performers: "00 오케스트라 / 00 무용단",
            audienceTrend: [4000, 4200, 4500, 4700, 4900],
            marketingBreakdown: [
              { category: "온라인 홍보", value: 25 },
              { category: "지역문화홍보", value: 15 },
              { category: "기타 마케팅", value: 10 },
            ],
        };

        return NextResponse.json(PlanningSummary);
    } catch (error) {
        console.error("Azure OpenAI Service 호출 에러:", error);
        return NextResponse.json({ error: "서버 에러 "}, { status: 500 });
    }
}