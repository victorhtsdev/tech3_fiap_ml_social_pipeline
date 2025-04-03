import React, { useEffect, useState } from "react";
import {
  getWordCloud,
  getSvmCategoryCounts,
  getCategoryColors,
} from "../../services/api";
import BarChart from "../BarChart/BarChart";
import WordCards from "../WordCards/WordCards";
import Legend from "../Legend/Legend";
import Scatter3D from "../Scatter3D/Scatter3D";
import ContentTable from "../ContentTable/ContentTable";
import TimeSeriesChart from "../TimeSeriesChart/TimeSeriesChart";
import {
  CategoryAnalysisContainer,
  ChartContainer,
  BackButton,
  AnimatedBlock,
} from "./styles";
import { ArrowLeft } from "lucide-react";

const CategoryAnalysis = ({ execId, onBack }) => {
  const [wordCloudData, setWordCloudData] = useState({});
  const [svmData, setSvmData] = useState([]);
  const [categoryColors, setCategoryColors] = useState({});
  const [hiddenCategories, setHiddenCategories] = useState(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [wordCloudResponse, svmResponse, colorsResponse] =
          await Promise.all([
            getWordCloud(execId),
            getSvmCategoryCounts(execId),
            getCategoryColors(execId),
          ]);

        setWordCloudData(wordCloudResponse);
        setCategoryColors(colorsResponse || {});
        setSvmData(
          svmResponse.map((item) => ({
            ...item,
            color: colorsResponse[item.label] || "#000000",
          }))
        );
      } catch (error) {
        console.error("🚨 Erro ao buscar os dados:", error);
      }
    };

    if (execId) {
      fetchData();
      const timer = setTimeout(() => {
        setLoading(false);
      }, 3000);
      return () => clearTimeout(timer);
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
      <BackButton onClick={onBack}>
        <ArrowLeft size={18} style={{ marginRight: 6 }} /> Back
      </BackButton>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <AnimatedBlock>
            <Legend
              categories={svmData.map(({ label, color }) => ({
                label,
                color,
              }))}
              hiddenCategories={hiddenCategories}
              toggleCategory={toggleCategory}
            />
          </AnimatedBlock>

          <AnimatedBlock>
            <ChartContainer>
              <BarChart data={svmData} hiddenCategories={hiddenCategories} />
            </ChartContainer>
          </AnimatedBlock>

          <AnimatedBlock>
            <ChartContainer>
             <TimeSeriesChart execId={execId} hiddenCategories={hiddenCategories} />
            </ChartContainer>
          </AnimatedBlock>

          <AnimatedBlock>
            <ContentTable execId={execId} categories={svmData} />
          </AnimatedBlock>

          <AnimatedBlock>
            <WordCards
              data={wordCloudData}
              hiddenCategories={hiddenCategories}
            />
          </AnimatedBlock>

          <AnimatedBlock>
            <Scatter3D
              execId={execId}
              categoryColors={categoryColors}
              hiddenCategories={hiddenCategories}
            />
          </AnimatedBlock>
        </>
      )}
    </CategoryAnalysisContainer>
  );
};

export default CategoryAnalysis;
