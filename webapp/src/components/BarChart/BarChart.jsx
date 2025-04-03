import React from "react";
import Plot from "react-plotly.js";
import { ChartContainer, ChartTitle, ChartDescription } from "./styles";

const BarChart = ({ data, hiddenCategories }) => {
  const filteredData = data.filter(({ label }) => !hiddenCategories.has(label));
  const totalFrases = filteredData.reduce((sum, item) => sum + item.count, 0);

  return (
    <ChartContainer>
      <ChartTitle>Distribuição de Categorias</ChartTitle>
      <ChartDescription>
        Este gráfico exibe a frequência das previsões feitas pelo modelo de machine learning para cada categoria. 
        Os comentários foram quebrados em frases e cada unidade representa uma frase do comentário.
      </ChartDescription>

      {filteredData.length > 0 ? (
        <>
          <p><strong>Total de frases analisadas:</strong> {totalFrases}</p>
          <Plot
            data={[
              {
                x: filteredData.map(({ label }) => label),
                y: filteredData.map(({ count }) => count),
                type: "bar",
                marker: { color: filteredData.map(({ color }) => color) },
                hoverinfo: "x+y",
                transition: { duration: 800, easing: "cubic-in-out" },
              },
            ]}
            layout={{
              xaxis: { title: "Categorias", tickangle: -30 },
              yaxis: { title: "Número de Previsões" },
              autosize: true,
              margin: { l: 50, r: 20, b: 100, t: 50 },
              barmode: "group",
              bargap: 0.3,
              responsive: true,
            }}
            useResizeHandler={true}
            style={{ width: "100%", height: "auto", minHeight: "400px" }}
          />
        </>
      ) : (
        <p>Sem dados para exibir.</p>
      )}
    </ChartContainer>
  );
};

export default BarChart;
