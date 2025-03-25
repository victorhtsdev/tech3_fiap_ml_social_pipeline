import React from "react";
import { LegendContainer, LegendItem } from "./styles";

const Legend = ({ categories, hiddenCategories, toggleCategory }) => {
  return (
    <LegendContainer>
      {categories.map(({ label, color }) => (
        <LegendItem
          key={label}
          active={!hiddenCategories.has(label)}
          style={{ backgroundColor: hiddenCategories.has(label) ? "#ccc" : color }}
          onClick={() => toggleCategory(label)}
        >
          {label}
        </LegendItem>
      ))}
    </LegendContainer>
  );
};

export default Legend;
