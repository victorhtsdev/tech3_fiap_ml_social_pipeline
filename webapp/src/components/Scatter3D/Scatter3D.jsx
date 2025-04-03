import React, { useEffect, useState, useMemo } from "react";
import Plot from "react-plotly.js";
import {
  ScatterContainer,
  HighlightCard,
  ChartTitle,
  ChartDescription,
  ScatterWrapper
} from "./styles";
import api from "../../services/api"; 

const Scatter3D = ({ execId, categoryColors, hiddenCategories }) => {
  const [data, setData] = useState([]);
  const [selectedComment, setSelectedComment] = useState(null);

  useEffect(() => {
    const fetchEmbeddings = async () => {
      try {
        const response = await api.get(`/get_embeddings?exec_id=${execId}`);
        const jsonData = response.data;

        if (!jsonData || jsonData.length === 0) {
          console.error("Nenhum dado recebido da API.");
          return;
        }

        const enrichedData = jsonData.map((item, index) => ({
          ...item,
          pointIndex: index,
        }));

        setData(enrichedData);
      } catch (error) {
        console.error("Erro ao buscar os embeddings:", error);
      }
    };

    if (execId) {
      fetchEmbeddings();
    }
  }, [execId]);

  const filteredData = useMemo(() => {
    return data.filter(({ label }) => !hiddenCategories.has(label));
  }, [data, hiddenCategories]);

  const fetchCommentHighlight = async (contentId) => {
    try {
      const response = await api.get(
        `/get_content_highlight?exec_id=${execId}&content_id=${contentId}`
      );
      const jsonData = response.data;

      if (jsonData.error) {
        console.error("Erro ao buscar o comentário:", jsonData.error);
      } else {
        setSelectedComment(jsonData);
      }
    } catch (error) {
      console.error("Erro na API de comentário:", error);
    }
  };

  return (
    <ScatterWrapper>
      <ChartTitle>Distribuição dos Dados no Espaço Vetorial</ChartTitle>
      <ChartDescription>
        Este gráfico exibe a organização dos embeddings das sentenças rotuladas pelo modelo de machine learning. 
        A posição dos pontos representa relações semânticas no espaço vetorial, enquanto as cores indicam as categorias identificadas.
      </ChartDescription>

      <ScatterContainer>
        {filteredData.length > 0 ? (
          <Plot
            data={[
              {
                x: filteredData.map(item => item.embedding[0]),
                y: filteredData.map(item => item.embedding[1]),
                z: filteredData.map(item => item.embedding[2] || 0),
                text: filteredData.map(item => `Label: ${item.label}<br>Texto: ${item.sentence}`),
                mode: "markers",
                marker: {
                  size: 5,
                  color: filteredData.map(item => categoryColors[item.label] || "#000000"),
                  showscale: false,
                },
                type: "scatter3d",
              },
            ]}
            layout={{
              margin: { l: 0, r: 0, b: 0, t: 20 },
              scene: {
                xaxis: { title: "Dimensão 1" },
                yaxis: { title: "Dimensão 2" },
                zaxis: { title: "Dimensão 3" },
              },
            }}
            config={{
              responsive: true,
              displayModeBar: false,
            }}
            style={{ width: "100%", height: "400px", maxWidth: "100%" }}
            onClick={(event) => {
              if (!event.points || event.points.length === 0) return;

              const pointIndex = event.points[0].pointIndex;
              const selectedData = filteredData[pointIndex];

              if (selectedData && selectedData.content_id) {
                fetchCommentHighlight(selectedData.content_id);
              } else {
                console.error("Content ID não encontrado no ponto selecionado.");
              }
            }}
          />
        ) : (
          <p>Sem dados para exibir.</p>
        )}
      </ScatterContainer>

      {selectedComment && (
        <HighlightCard>
          <h3>Comentário Destacado</h3>
          <p>{selectedComment.content}</p>
          {selectedComment.highlights.map((highlight, index) => (
            <span key={index} style={{ backgroundColor: highlight.color, padding: "2px 4px", borderRadius: "4px", margin: "2px" }}>
              {highlight.fragment}
            </span>
          ))}
        </HighlightCard>
      )}
    </ScatterWrapper>
  );
};

export default Scatter3D;
