// components/ChartBar.js
'use client';

import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function ChartBar({ data }) {
    const ref = useRef();

    useEffect(() => {
        const chartData = data && data.length ? data : [
            { category: '온라인 홍보', value: 25 },
            { category: '지역문화홍보', value: 15 },
            { category: '기타 마케팅', value: 10 },
        ];
        const margin = { top: 20, right: 20, bottom: 30, left: 60 };
        const width = 600;
        const height = 300;

        const container = d3.select(ref.current);
        container.selectAll('*').remove();

        const svg = container
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const x = d3.scaleLinear()
            .domain([0, d3.max(chartData, d => d.value)])
            .range([margin.left, width - margin.right]);

        const y = d3.scaleBand()
            .domain(chartData.map(d => d.category))
            .range([margin.top, height - margin.bottom])
            .padding(0.1);

        svg.append('g')
            .attr('transform', `translate(0,${margin.top})`)
            .call(d3.axisTop(x).ticks(5));
        svg.append('g')
            .attr('transform', `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));

        svg.selectAll('.bar')
            .data(chartData)
            .enter()
            .append('rect')
            .attr('class', 'bar fill-blue-500')
            .attr('x', margin.left)
            .attr('y', d => y(d.category))
            .attr('width', d => x(d.value) - margin.left)
            .attr('height', y.bandwidth());
    }, [data]);
    
    return <div ref={ref} />;
}
