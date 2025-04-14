// charts.js

// Pie Chart 1 - 예산 분포
(function renderPieChart1() {
    const svg = d3.select("#pieChart1"),
      width = +svg.attr("width") || 300,
      height = +svg.attr("height") || 300,
      radius = Math.min(width, height) / 2;
  
    const g = svg
      .append("g")
      .attr("transform", `translate(${width / 2},${height / 2})`);
  
    const color = d3.scaleOrdinal(d3.schemeCategory10);
  
    const pie = d3.pie().value(d => d.value);
  
    const data = [
      { label: "들입료", value: 24 },
      { label: "무대/조명/음향", value: 6 },
      { label: "홍보", value: 4 },
      { label: "대관료", value: 1 }
    ];
  
    const arc = d3.arc().innerRadius(0).outerRadius(radius);
  
    const arcs = g.selectAll("arc")
      .data(pie(data))
      .enter()
      .append("g");
  
    arcs.append("path")
      .attr("d", arc)
      .attr("fill", d => color(d.data.label));
  
    arcs.append("text")
      .attr("transform", d => `translate(${arc.centroid(d)})`)
      .attr("text-anchor", "middle")
      .text(d => d.data.label);
  })();
  
  // Bar Chart - 지원사업 참여도
  (function renderBarChart() {
    const data = [
      { label: "문예회관 정기공모", value: 70 },
      { label: "지역문예진단 지원", value: 40 },
      { label: "기업 메세나", value: 80 }
    ];
  
    const svg = d3.select("#barChart"),
      width = +svg.attr("width") || 300,
      height = +svg.attr("height") || 300;
  
    const margin = { top: 20, right: 30, bottom: 40, left: 100 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
  
    const x = d3.scaleLinear().domain([0, 100]).range([0, chartWidth]);
    const y = d3.scaleBand()
      .domain(data.map(d => d.label))
      .range([0, chartHeight])
      .padding(0.3);
  
    const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  
    g.append("g")
      .call(d3.axisLeft(y));
  
    g.selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("y", d => y(d.label))
      .attr("height", y.bandwidth())
      .attr("width", d => x(d.value))
      .attr("fill", "#69b3a2");
  })();
  