// components/ChartPie.js
'use client';

import { useEffect, useRef } from "react";
import * as d3 from 'd3';

export default function ChartPie({ data }) {
    const ref = useRef();

    useEffect(() => {
        const chartData = data && data.length ? data : [
            { category: 'A', value: 10 },
            { category: 'B', value: 20 },
            { category: 'C', value: 30 },
        ];

        const width = 200;
        const height = 200;
        const margin = 10;
        const radius = Math.min(width, height) /  2 - margin;

        const container = d3.select(ref.current);
        container.selectAll('*').remove();

        const svg = container
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);

        const color = d3.scaleOrdinal()
            .domain(chartData.map(d => d.category))
            .range(d3.schemeSet2);
      
        const pie = d3.pie().value(d => d.value);
        const data_ready = pie(chartData);
      
        svg.selectAll('path')
            .data(data_ready)
            .enter()
            .append('path')
            .attr('d', d3.arc()
              .innerRadius(0)
              .outerRadius(radius)
            )
            .attr('fill', d => color(d.data.category))
            .attr('stroke', 'white')
            .style('stroke-width', '2px');
    }, [data]);
      
    return <div ref={ref} />;
}
      