import React, { useState } from "react";
import { ControlPanelContainer } from "./styles";
import ControlButton from "../ControlButton/ControlButton";
import NewAnalysisScreen from "../NewAnalysisScreen/NewAnalysisScreen";

const ControlPanel = ({ searchTerm, selectedItem, refreshSidebar, setReloadAnalysisList, openModelExplorer }) => {
  const [showModal, setShowModal] = useState(false);
  console.log("🔧 Props do ControlPanel:", { openModelExplorer });

  return (
    <ControlPanelContainer>
      <ControlButton 
        searchTerm={searchTerm}
        selectedItem={selectedItem}
        onClick={() => setShowModal(true)}
        icon="plus"
        label="New Analysis"
        requireSelection={true}
      />
      <ControlButton
  onClick={() => {
    console.log("✅ Botão Model Explorer clicado");
    if (openModelExplorer) {
      openModelExplorer();
    } else {
      console.log("❌ openModelExplorer está undefined!");
    }
  }}
  icon="bar-chart-3"
  label="Model Explorer"
/>
      <NewAnalysisScreen
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        searchTerm={selectedItem?.name || searchTerm}
        refreshSidebar={refreshSidebar}
        setReloadAnalysisList={setReloadAnalysisList}
      />
    </ControlPanelContainer>
  );
};

export default ControlPanel;
