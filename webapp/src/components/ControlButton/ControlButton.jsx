import React from "react";
import { ButtonContainer } from "./styles";
import { Plus } from "lucide-react";

const ControlButton = ({ searchTerm, selectedItem, onClick }) => {
  const isDisabled = !searchTerm && !selectedItem;
  const buttonLabel = "New Analysis";

  return (
    <ButtonContainer disabled={isDisabled} onClick={onClick}>
      <Plus size={16} />
      {buttonLabel}
    </ButtonContainer>
  );
};

export default ControlButton;
