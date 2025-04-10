// components/ChartLine.js
'use client';

import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function ChartLine({ data }) {
    const ref = useRef();

    useEffect(() => {
        const chartData = data && data.length ? data : [1000, 1200, 1500, 1700, 2000];
        const margin = { top: 20, right: 20, bottom: 30, left: 40 };
        const width = 600;
        const height = 300;

        const container = d3.select(ref.current);
        container.selectAll('*').remove();

        const svg = container
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        const x = d3.scaleLinear()
            .domain([0, chartData.length - 1])
            .range([margin.left, width - margin.right]);

        const y = d3.scaleLinear()
            .domain([0, d3.max(chartData)])
            .nice()
            .range([height - margin.bottom, margin.top]);

        const line = d3.line()
            .x((_, i) => x(i))
            .y(d => y(d));

        svg.append('g')
            .attr('transform', `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x).ticks(chartData.length));
        svg.append('g')
            .attr('transform', `translate(${margin.left},0)`)
            .call(d3.axisLeft(y));

        svg.append('path')
            .datum(chartData)
            .attr('fill', 'none')
            .attr('stroke', '#8884d8')
            .attr('stroke-width', 2)
            .attr('d', line);
        }, [data]);

    return <div ref={ref} />;
}
