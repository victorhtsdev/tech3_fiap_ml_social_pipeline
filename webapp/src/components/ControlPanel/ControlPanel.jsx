import React, { useState } from "react";
import { ControlPanelContainer } from "./styles";
import ControlButton from "../ControlButton/ControlButton";
import NewAnalysisScreen from "../NewAnalysisScreen/NewAnalysisScreen";

const ControlPanel = ({ searchTerm, selectedItem, refreshSidebar, setReloadAnalysisList }) => {
  const [showModal, setShowModal] = useState(false);

  return (
    <ControlPanelContainer>
      <ControlButton 
        searchTerm={searchTerm}
        selectedItem={selectedItem}
        onClick={() => setShowModal(true)}
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
