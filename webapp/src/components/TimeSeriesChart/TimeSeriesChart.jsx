import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { ChartContainer, ChartTitle, ChartDescription } from "./styles";
import { getTimeSeriesLabel } from "../../services/api";

const TimeSeriesChart = ({ execId, hiddenCategories }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchSeries = async () => {
      try {
        const response = await getTimeSeriesLabel(execId);
        setData(response);
      } catch (error) {
        console.error("❌ Error loading time series:", error);
      }
    };

    if (execId) fetchSeries();
  }, [execId]);

  const grouped = data.reduce((acc, item) => {
    if (!acc[item.label]) acc[item.label] = { x: [], y: [], color: item.color };
    acc[item.label].x.push(item.date);
    acc[item.label].y.push(item.count);
    return acc;
  }, {});

  const traces = Object.entries(grouped)
    .filter(([label]) => !hiddenCategories?.has(label))
    .map(([label, { x, y, color }]) => ({
      x,
      y,
      type: "scatter",
      mode: "lines+markers",
      name: label,
      marker: { color },
      line: { color },
    }));

  return (
    <ChartContainer>
      <ChartTitle>Evolução Temporal por Categoria</ChartTitle>
      <ChartDescription>
        Este gráfico mostra a quantidade de frases classificadas por categoria ao longo do tempo.
      </ChartDescription>

      {traces.length > 0 ? (
        <Plot
          data={traces}
          layout={{
            xaxis: { title: "Data" },
            yaxis: { title: "Número de Frases" },
            autosize: true,
            margin: { l: 50, r: 20, b: 80, t: 50 },
            legend: { orientation: "h" },
            responsive: true,
          }}
          useResizeHandler={true}
          style={{ width: "100%", height: "auto", minHeight: "400px" }}
        />
      ) : (
        <p>Sem dados disponíveis para exibir.</p>
      )}
    </ChartContainer>
  );
};

export default TimeSeriesChart;
