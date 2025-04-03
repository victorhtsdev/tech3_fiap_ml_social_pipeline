import React, { useState, useEffect, useCallback } from "react";
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
  PipelineWrapper,
} from "./styles";
import { Folder, CalendarDays, Clock, Trash2 } from "lucide-react";
import PipelineStatus from "../PipelineStatus/PipelineStatus";
import {
  getAnalysesBySearch,
  deleteAnalysisByExecId,
} from "../../services/api";

const AnalysisList = ({ searchTerm, onSelectAnalysis, reloadTrigger }) => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);

  const fetchAnalyses = useCallback(async () => {
    if (!searchTerm) return;
    setLoading(true);
    const data = await getAnalysesBySearch(searchTerm);
    setAnalyses(data);
    setLoading(false);
  }, [searchTerm]);

  useEffect(() => {
    fetchAnalyses();
  }, [fetchAnalyses, reloadTrigger]);

  const getDateRange = (ranges) => {
    if (ranges.length === 0) return "No ranges";
    return `${ranges[0][0]} - ${ranges[ranges.length - 1][1]}`;
  };

  const handleDelete = async (event, execId) => {
    event.stopPropagation();
    const confirmed = window.confirm(
      "Are you sure you want to delete this analysis?"
    );
    if (!confirmed) return;

    try {
      await deleteAnalysisByExecId(execId);
      setAnalyses((prev) => prev.filter((item) => item.id !== execId));
    } catch (error) {
      console.error("❌ Error deleting analysis:", error);
      alert("Failed to delete analysis.");
    }
  };

  return (
    <ResponsiveWrapper>
      <AnalysisContainer>
        {loading ? (
          <p>Loading...</p>
        ) : analyses.length === 0 ? (
          <p>No analyses found.</p>
        ) : (
          analyses.map((analysis) => (
            <AnalysisCard
              key={analysis.id}
              onClick={() => onSelectAnalysis(analysis)}
              onMouseEnter={() => setSelectedAnalysis(analysis)}
              className={selectedAnalysis?.id === analysis.id ? "active" : ""}
            >
              <AnalysisContent>
                <AnalysisTitle>
                  <Folder
                    size={18}
                    style={{ marginRight: 8, color: "#4f46e5" }}
                  />
                  {analysis.classification_model_name} (
                  {analysis.classification_model_type}) - v
                  {analysis.classification_model_version}
                  <Trash2
                    size={16}
                    style={{
                      marginLeft: "auto",
                      color: "#ef4444",
                      cursor: "pointer",
                    }}
                    onClick={(e) => handleDelete(e, analysis.id)}
                    title="Delete analysis"
                  />
                </AnalysisTitle>
                <AnalysisDetails>
                  <div>
                    <AnalysisLabel>
                      <CalendarDays
                        size={14}
                        style={{ marginRight: 5, color: "#6b7280" }}
                      />
                      Date:
                    </AnalysisLabel>
                    <AnalysisDate>{analysis.date}</AnalysisDate>
                  </div>
                  <div>
                    <AnalysisLabel>
                      <Clock
                        size={14}
                        style={{ marginRight: 5, color: "#6b7280" }}
                      />
                      Period:
                    </AnalysisLabel>
                    <AnalysisRanges>
                      {(() => {
                        try {
                          const ranges = JSON.parse(analysis.date_ranges);
                          return getDateRange(ranges);
                        } catch {
                          return "Invalid period";
                        }
                      })()}
                    </AnalysisRanges>
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
