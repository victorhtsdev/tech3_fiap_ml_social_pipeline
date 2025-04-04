import React, { useEffect, useState, useRef } from "react";
import Plot from "react-plotly.js";
import { motion } from "framer-motion";
import { ChartContainer, ChartTitle, ChartDescription } from "./styles";
import { getTimeSeriesLabel } from "../../services/api";

const TimeSeriesChart = ({ execId, hiddenCategories }) => {
  const [data, setData] = useState([]);
  const [annotations, setAnnotations] = useState([]);
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [markerText, setMarkerText] = useState("");
  const popupRef = useRef(null);

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

  const handleClick = (event) => {
    const point = event.points?.[0];
    if (point) {
      const { x, y } = point;
      setSelectedPoint({ x, y });
      setMarkerText("");
    }
  };

  const handleAddMarker = () => {
    if (selectedPoint && markerText) {
      setAnnotations((prev) => [
        ...prev,
        {
          x: selectedPoint.x,
          y: selectedPoint.y,
          text: markerText,
        },
      ]);
      setSelectedPoint(null);
      setMarkerText("");
    }
  };

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (popupRef.current && !popupRef.current.contains(e.target)) {
        setSelectedPoint(null);
        setMarkerText("");
      }
    };

    if (selectedPoint) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [selectedPoint]);

  return (
    <ChartContainer>
      <ChartTitle>Evolução Temporal por Categoria</ChartTitle>
      <ChartDescription>
        Este gráfico mostra a quantidade de frases classificadas por categoria ao longo do tempo.
      </ChartDescription>

      {selectedPoint && (
        <motion.div
          ref={popupRef}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.2 }}
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            background: "#fff",
            border: "1px solid #ccc",
            borderRadius: "12px",
            padding: "16px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.2)",
            zIndex: 1000,
            width: "320px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div style={{ marginBottom: "10px", fontWeight: 600, fontSize: "16px", textAlign: "center" }}>
            Marcador para ({new Date(selectedPoint.x).toLocaleDateString("pt-BR")}, {selectedPoint.y})
          </div>
          <input
            type="text"
            value={markerText}
            onChange={(e) => setMarkerText(e.target.value)}
            placeholder="Digite o texto do marcador"
            style={{
              width: "100%",
              padding: "8px",
              border: "1px solid #aaa",
              borderRadius: "6px",
              marginBottom: "12px",
              fontSize: "14px",
            }}
          />
          <button
            onClick={handleAddMarker}
            style={{
              background: "transparent",
              color: "rgb(58, 91, 237)",
              padding: "6px 14px",
              border: "1px solid rgb(58, 91, 237)",
              borderRadius: "6px",
              cursor: "pointer",
              fontWeight: 600,
              fontSize: "14px",
            }}
          >
            Adicionar
          </button>
        </motion.div>
      )}

      {traces.length > 0 ? (
        <Plot
          data={traces}
          layout={{
            xaxis: {
              title: "Data",
              tickformat: "%d/%m/%Y",
            },
            yaxis: { title: "Número de Frases" },
            autosize: true,
            margin: { l: 50, r: 20, b: 80, t: 50 },
            legend: { orientation: "h" },
            responsive: true,
            annotations: annotations.map((a) => ({
              x: a.x,
              y: a.y,
              text: a.text,
              showarrow: true,
              arrowhead: 4,
              ax: 0,
              ay: -40,
              bgcolor: "rgba(255,255,255,0.9)",
              bordercolor: "#888",
              borderwidth: 1,
              font: {
                color: "#000",
                size: 12,
              },
            })),
          }}
          useResizeHandler={true}
          style={{ width: "100%", height: "auto", minHeight: "400px" }}
          onClick={handleClick}
        />
      ) : (
        <p>Sem dados disponíveis para exibir.</p>
      )}
    </ChartContainer>
  );
};

export default TimeSeriesChart;
