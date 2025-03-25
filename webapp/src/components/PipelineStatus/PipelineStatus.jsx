import React, { useState, useEffect } from "react";
import "./PipelineStatus.css";
import { getPipelineStatus } from "../../services/api";

const PipelineStatus = ({ selectedItem }) => {
  const [stages, setStages] = useState([]);

  useEffect(() => {
    if (!selectedItem) {
      setStages([]);
      return;
    }

    const fetchStatus = async () => {
      const data = await getPipelineStatus(selectedItem.id);
      if (data) {
        console.log("Pipeline Status recebido:", data.stages);
        setStages(
          data.stages.map(stage => ({
            ...stage,
            status: stage.status
              ? stage.status.toLowerCase().replace("completed", "success").replace("not started", "not-started")
              : "not-started"
          }))
        );
      }
    };

    fetchStatus();

    const interval = setInterval(() => {
      fetchStatus();
    }, 5000);

    return () => clearInterval(interval);
  }, [selectedItem]);

  return (
    <div className="pipeline-container">
      {stages.length > 0 ? (
        stages.map((stage, index) => (
          <div key={index} className="pipeline-step">
            <div className={`status-indicator ${stage.status}`}></div>
            {stage.name}
          </div>
        ))
      ) : (
        <p>Selecione um item para visualizar o status.</p>
      )}
    </div>
  );
};

export default PipelineStatus;
