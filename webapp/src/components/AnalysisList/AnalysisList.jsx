import React, { useState, useEffect } from "react";
import { 
  AnalysisContainer, 
  AnalysisCard, 
  AnalysisContent, 
  AnalysisTitle, 
  AnalysisDetails, 
  AnalysisLabel, 
  AnalysisDate, 
  AnalysisRanges, 
  ResponsiveWrapper, 
  PipelineWrapper 
} from "./styles";
import { Folder, CalendarDays, Clock } from "lucide-react";
import PipelineStatus from "../PipelineStatus/PipelineStatus";
import { getAnalysesBySearch } from "../../services/api";

const AnalysisList = ({ searchTerm, onSelectAnalysis }) => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);

  useEffect(() => {
    if (!searchTerm) return;
    setLoading(true);

    const fetchAnalyses = async () => {
      const data = await getAnalysesBySearch(searchTerm);
      setAnalyses(data);
      setLoading(false);
    };

    fetchAnalyses();
  }, [searchTerm]);

  const getDateRange = (ranges) => {
    if (ranges.length === 0) return "No ranges";
    return `${ranges[0][0]} - ${ranges[ranges.length - 1][1]}`;
  };

  return (
    <ResponsiveWrapper>
      <AnalysisContainer>
        {loading ? (
          <p>Carregando análises...</p>
        ) : analyses.length === 0 ? (
          <p>Nenhuma análise encontrada.</p>
        ) : (
          analyses.map((analysis) => (
            <AnalysisCard 
              key={analysis.id} 
              onClick={() => onSelectAnalysis(analysis)} // 🔥 Envia para o App.jsx
              onMouseEnter={() => setSelectedAnalysis(analysis)} 
              className={selectedAnalysis?.id === analysis.id ? "active" : ""}
            >
              <AnalysisContent>
                <AnalysisTitle>
                  <Folder size={18} style={{ marginRight: 8, color: "#4f46e5" }} />
                  {analysis.classification_model_name} ({analysis.classification_model_type}) 
                  - v{analysis.classification_model_version}
                </AnalysisTitle>
                <AnalysisDetails>
                  <div>
                    <AnalysisLabel>
                      <CalendarDays size={14} style={{ marginRight: 5, color: "#6b7280" }} /> 
                      Data:
                    </AnalysisLabel>
                    <AnalysisDate>{analysis.date}</AnalysisDate>
                  </div>
                  <div>
                    <AnalysisLabel>
                      <Clock size={14} style={{ marginRight: 5, color: "#6b7280" }} /> 
                      Período:
                    </AnalysisLabel>
                    <AnalysisRanges>{getDateRange(analysis.date_ranges)}</AnalysisRanges>
                  </div>
                </AnalysisDetails>
              </AnalysisContent>
            </AnalysisCard>
          ))
        )}
      </AnalysisContainer>

      <PipelineWrapper>
        {selectedAnalysis && <PipelineStatus selectedItem={selectedAnalysis} />}
      </PipelineWrapper>
    </ResponsiveWrapper>
  );
};

export default AnalysisList;
