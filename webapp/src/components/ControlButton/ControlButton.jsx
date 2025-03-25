import React from "react";
import { ButtonContainer } from "./styles";
import { Plus } from "lucide-react";
import { runPipeline } from "../../services/api";

const ControlButton = ({ searchTerm, selectedItem, refreshSidebar }) => {
  const isDisabled = !searchTerm && !selectedItem;
  const buttonLabel = selectedItem ? "New Version" : "New Pipeline";


  const searchValue = selectedItem ? selectedItem.name : searchTerm;

  const handleClick = async () => {
    if (!searchValue || searchValue.trim() === "") {
      alert("❌ No search term provided.");
      return;
    }

    try {
      const response = await runPipeline({ search: searchValue });
      alert(`✅ ${response.message}\nExec ID: ${response.exec_id || "N/A"}`);

      if (!selectedItem) {
        refreshSidebar();
      }
    } catch (error) {
      alert("❌ Error running pipeline.");
      console.error(error);
    }
  };

  return (
    <ButtonContainer disabled={isDisabled} onClick={handleClick}>
      <Plus size={16} />
      {buttonLabel}
    </ButtonContainer>
  );
};

export default ControlButton;