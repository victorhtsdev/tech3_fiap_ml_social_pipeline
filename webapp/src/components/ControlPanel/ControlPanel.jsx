import React from "react";
import { ControlPanelContainer } from "./styles";
import ControlButton from "../ControlButton/ControlButton";

const ControlPanel = ({ searchTerm, selectedItem, refreshSidebar }) => {

  console.log("ControlPanel - searchTerm:", searchTerm);
  console.log("ControlPanel - selectedItem:", selectedItem);

  return (
    <ControlPanelContainer>
      <ControlButton 
        searchTerm={searchTerm} 
        selectedItem={selectedItem} 
        refreshSidebar={refreshSidebar} 
      />
    </ControlPanelContainer>
  );
};

export default ControlPanel;