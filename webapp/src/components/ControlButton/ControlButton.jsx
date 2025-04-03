import React from "react";
import { ButtonContainer } from "./styles";
import { Plus, BarChart3 } from "lucide-react";

const icons = {
  plus: <Plus size={16} />,
  "bar-chart-3": <BarChart3 size={16} />
};

const ControlButton = ({
  searchTerm,
  selectedItem,
  onClick,
  icon = "plus",
  label = "New Analysis",
  requireSelection = false
}) => {
  const isDisabled = requireSelection
    ? !selectedItem && !searchTerm
    : false;

  return (
    <ButtonContainer disabled={isDisabled} onClick={onClick}>
      {icons[icon]}
      {label}
    </ButtonContainer>
  );
};

export default ControlButton;
