import React from "react";
import Plot from "react-plotly.js";
import {
  ChartContainer,
  ChartTitle,
  ChartExplanation,
  ChartNote
} from "./styles";

const ModelComparisonChart = ({ data }) => {
  if (!data || data.length === 0) return <p>Sem dados para exibir.</p>;

  const scores = ["Accuracy", "Macro Avg (F1)", "Weighted Avg (F1)"];
  const svm = data.find(m => m.model_name.toLowerCase() === "svm");
  const xgb = data.find(m => m.model_name.toLowerCase().includes("xgboost"));

  const format = (value) => Math.round(value * 100);

  return (
    <ChartContainer>
      <ChartTitle>Avaliação do Desempenho dos Modelos</ChartTitle>
      <ChartExplanation>
        Esta seção compara os modelos <strong>SVM</strong> e <strong>XGBoost</strong> com base em três métricas principais:<br />
        <strong>Accuracy</strong> (proporção de acertos), <strong>Macro F1</strong> (média simples entre classes) e <strong>Weighted F1</strong> (média ponderada pelo tamanho das classes).<br />
        Em cenários com classes desbalanceadas, o <strong>Weighted F1</strong> costuma ser a métrica mais confiável.
      </ChartExplanation>

      <ChartNote>
        <strong>Gráfico comparando os scores globais por modelo:</strong>
      </ChartNote>

      <Plot
        data={[
          {
            x: scores,
            y: [
              svm?.global_metrics.accuracy || 0,
              svm?.global_metrics.macro_f1 || 0,
              svm?.global_metrics.weighted_f1 || 0
            ],
            name: "SVM",
            type: "bar",
            marker: { color: "#E69F00" },
            text: [
              format(svm?.global_metrics.accuracy),
              format(svm?.global_metrics.macro_f1),
              format(svm?.global_metrics.weighted_f1)
            ],
            textposition: "auto"
          },
          {
            x: scores,
            y: [
              xgb?.global_metrics.accuracy || 0,
              xgb?.global_metrics.macro_f1 || 0,
              xgb?.global_metrics.weighted_f1 || 0
            ],
            name: "XGBoost",
            type: "bar",
            marker: { color: "#56B4E9" },
            text: [
              format(xgb?.global_metrics.accuracy),
              format(xgb?.global_metrics.macro_f1),
              format(xgb?.global_metrics.weighted_f1)
            ],
            textposition: "auto"
          }
        ]}
        layout={{
          barmode: "group",
          xaxis: { title: "Métricas" },
          yaxis: { title: "Score", range: [0, 1] },
          bargap: 0.25,
          bargroupgap: 0.1,
          autosize: true,
          margin: { l: 50, r: 20, b: 80, t: 40 },
          showlegend: true,
          legend: { orientation: "h", x: 0.5, xanchor: "center", y: -0.2 },
          hovermode: "x unified"
        }}
        useResizeHandler={true}
        style={{ width: "100%", height: "auto", minHeight: "400px" }}
      />
    </ChartContainer>
  );
};

export default ModelComparisonChart;
