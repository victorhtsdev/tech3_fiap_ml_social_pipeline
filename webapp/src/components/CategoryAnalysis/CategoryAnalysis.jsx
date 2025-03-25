import React, { useEffect, useState } from "react";
import { getWordCloud, getSvmCategoryCounts, getCategoryColors } from "../../services/api";
import BarChart from "../BarChart/BarChart";
import WordCards from "../WordCards/WordCards";
import Legend from "../Legend/Legend";
import Scatter3D from "../Scatter3D/Scatter3D";
import { CategoryAnalysisContainer, ChartContainer, BackButton } from "./styles";
import { ArrowLeft } from "lucide-react"; // 🔹 Importando o ícone

const CategoryAnalysis = ({ execId, onBack }) => {
  const [wordCloudData, setWordCloudData] = useState({});
  const [svmData, setSvmData] = useState([]);
  const [categoryColors, setCategoryColors] = useState({});
  const [hiddenCategories, setHiddenCategories] = useState(new Set());

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [wordCloudResponse, svmResponse, colorsResponse] = await Promise.all([
          getWordCloud(execId),
          getSvmCategoryCounts(execId),
          getCategoryColors(execId)
        ]);

        setWordCloudData(wordCloudResponse);
        setCategoryColors(colorsResponse || {});
        setSvmData(svmResponse.map(item => ({
          ...item,
          color: colorsResponse[item.label] || "#000000",
        })));

      } catch (error) {
        console.error("🚨 Erro ao buscar os dados:", error);
      }
    };

    if (execId) {
      fetchData();
    }
  }, [execId]);

  const toggleCategory = (category) => {
    setHiddenCategories((prev) => {
      const newSet = new Set(prev);
      newSet.has(category) ? newSet.delete(category) : newSet.add(category);
      return newSet;
    });
  };

  return (
    <CategoryAnalysisContainer>
      {/* 🔙 Botão para voltar à lista com Ícone */}
      <BackButton onClick={onBack}>
        <ArrowLeft size={18} style={{ marginRight: 6 }} /> Voltar
      </BackButton>

      <Legend
        categories={svmData.map(({ label, color }) => ({ label, color }))}
        hiddenCategories={hiddenCategories}
        toggleCategory={toggleCategory}
      />
      <ChartContainer>
        <BarChart data={svmData} hiddenCategories={hiddenCategories} />
      </ChartContainer>
      <WordCards data={wordCloudData} hiddenCategories={hiddenCategories} />

      <Scatter3D execId={execId} categoryColors={categoryColors} hiddenCategories={hiddenCategories} />
    </CategoryAnalysisContainer>
  );
};

export default CategoryAnalysis;
