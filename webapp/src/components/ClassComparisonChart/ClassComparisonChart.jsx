import React from "react";
import Plot from "react-plotly.js";
import {
  ChartContainer,
  ChartTitle,
  ChartExplanation,
  ChartNote,
} from "./styles";

const ClassComparisonChart = ({ data }) => {
  if (!data || data.length === 0) return <p>Sem dados para exibir.</p>;

  const classes =
    data[0]?.class_metrics
      ?.filter(
        (c) => c.class_name !== "macro avg" && c.class_name !== "weighted avg"
      )
      ?.map((c) => c.class_name) || [];

  const svmScores = classes.map((className) => {
    const model = data.find((d) => d.model_name === "SVM");
    const entry = model?.class_metrics.find(
      (c) => c.class_name === className
    );
    return entry?.f1_score || null;
  });

  const xgbScores = classes.map((className) => {
    const model = data.find((d) => d.model_name === "XGBOOST");
    const entry = model?.class_metrics.find(
      (c) => c.class_name === className
    );
    return entry?.f1_score || null;
  });

  const z = classes.map((_, i) => [svmScores[i], xgbScores[i]]);
  const text = z.map(row => row.map(score => score?.toFixed(2)));

  return (
    <ChartContainer>
      <ChartTitle>Heatmap de F1-score por Classe</ChartTitle>
      <ChartExplanation>
        O mapa de calor apresenta o <strong>F1-score por classe</strong>, comparando os dois modelos:<br />
        <strong>Linhas</strong>: categorias (rótulos) – <strong>Colunas</strong>: modelo – <strong>Células</strong>: F1-score entre 0 e 1.
      </ChartExplanation>
      <ChartNote>
        <strong>
          Esse gráfico permite identificar em quais categorias cada modelo teve melhor desempenho, e onde há maior diferença entre eles.
        </strong>
      </ChartNote>

      <ChartContainer>
  <div style={{ display: "flex", justifyContent: "center" }}>
  <Plot
  data={[
    {
      z,
      x: ["SVM", "XGBoost"],
      y: classes,
      type: "heatmap",
      colorscale: "YlGnBu",
      reversescale: true,
      showscale: true,
      hoverinfo: "text",
      text: text,
    },
  ]}
  layout={{
    height: classes.length * 22 + 100,
    autosize: true,
    margin: { l: 160, r: 20, b: 60, t: 50 },
    xaxis: { title: "Modelo" },
    yaxis: { title: "Classe", automargin: true },
    font: { size: 12 },
    annotations: z.flatMap((row, i) =>
      row.map((score, j) => ({
        x: ["SVM", "XGBoost"][j],
        y: classes[i],
        text: score?.toFixed(2),
        font: {
          color: score > 0.7 ? "white" : "black",
          size: 11,
        },
        showarrow: false,
      }))
    ),
  }}
  config={{ responsive: true }}
  style={{ width: "50%" }}
/>

  </div>
</ChartContainer>

    </ChartContainer>
  );
};

export default ClassComparisonChart;
