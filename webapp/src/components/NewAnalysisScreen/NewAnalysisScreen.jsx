import React, { useEffect, useState, useRef } from "react";
import {
  ModalOverlay,
  ModalContainer,
  FieldGroup,
  Label,
  Select,
  DateInput,
  ConfirmButton,
  ModalTitle,
  CloseButton,
  DateRangeRow,
  AddButton,
  RemoveButton
} from "./styles";
import { getModelsInfo, runPipeline } from "../../services/api";

const NewAnalysisScreen = ({
  isOpen,
  onClose,
  searchTerm,
  refreshSidebar,
  setReloadAnalysisList
}) => {
  const [modelTypes, setModelTypes] = useState([]);
  const [modelsByType, setModelsByType] = useState({});
  const [selectedType, setSelectedType] = useState("");
  const [selectedModel, setSelectedModel] = useState(null);
  const [dateRanges, setDateRanges] = useState([{ start: "", end: "" }]);
  const [formValid, setFormValid] = useState(false);
  const localSearchTerm = useRef("");

  useEffect(() => {
    if (isOpen) {
      localSearchTerm.current = searchTerm || "";
      setSelectedType("");
      setSelectedModel(null);
      setDateRanges([{ start: "", end: "" }]);
      setFormValid(false);

      getModelsInfo().then((data) => {
        setModelTypes(data.types);
        setModelsByType(data.models);
      });
    }
  }, [isOpen, searchTerm]);

  useEffect(() => {
    const validate = () => {
      if (!selectedType || !selectedModel) return false;

      for (const range of dateRanges) {
        if (!range.start || !range.end) return false;

        const start = new Date(range.start);
        const end = new Date(range.end);

        if (isNaN(start.getTime()) || isNaN(end.getTime())) return false;
        if (end < start) return false;
      }

      return true;
    };

    setFormValid(validate());
  }, [selectedType, selectedModel, dateRanges]);

  const modelsForType = selectedType ? modelsByType[selectedType] || [] : [];

  const handleAddRange = () => {
    setDateRanges([...dateRanges, { start: "", end: "" }]);
  };

  const handleRemoveRange = (index) => {
    const updated = [...dateRanges];
    updated.splice(index, 1);
    setDateRanges(updated);
  };

  const handleDateChange = (index, field, value) => {
    const updated = [...dateRanges];
    updated[index][field] = value;

    if (field === "start" && value) {
      updated[index].end = value;
    }

    setDateRanges(updated);
  };

  const handleSubmit = async () => {
    const selected = modelsForType.find((m) => m.id === selectedModel);
    const modelLabelParts = selected?.label?.split(" - v") || [];

    const payload = {
      search: localSearchTerm.current,
      classification_model_name: modelLabelParts[0],
      classification_model_version: parseInt(modelLabelParts[1]),
      classification_model_type: selectedType,
      date_ranges: dateRanges.map((r) => [r.start, r.end])
    };

    try {
      const res = await runPipeline(payload);
      alert(`✅ ${res.message}\nExec ID: ${res.exec_id}`);

      if (typeof refreshSidebar === "function") {
        refreshSidebar();
      }

      if (typeof setReloadAnalysisList === "function") {
        setReloadAnalysisList((prev) => !prev);
      }

      onClose();
    } catch (error) {
      alert("❌ Error running pipeline.");
      console.error(error);
    }
  };

  if (!isOpen) return null;

  return (
    <ModalOverlay>
      <ModalContainer>
        <ModalTitle>New Analysis</ModalTitle>

        <FieldGroup>
          <Label>Model Type</Label>
          <Select
            value={selectedType}
            onChange={(e) => {
              setSelectedType(e.target.value);
              setSelectedModel("");
            }}
          >
            <option value="">Select a type</option>
            {modelTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </Select>
        </FieldGroup>

        <FieldGroup>
          <Label>Model</Label>
          <Select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            disabled={!selectedType}
          >
            <option value="">Select a model</option>
            {modelsForType.map((model) => (
              <option key={model.id} value={model.id}>
                {model.label}
              </option>
            ))}
          </Select>
        </FieldGroup>

        <Label>Date Ranges</Label>
        {dateRanges.map((range, index) => (
          <DateRangeRow key={index}>
            <DateInput
              type="date"
              value={range.start}
              onChange={(e) => handleDateChange(index, "start", e.target.value)}
            />
            <DateInput
              type="date"
              value={range.end}
              onChange={(e) => handleDateChange(index, "end", e.target.value)}
            />
            {dateRanges.length > 1 && (
              <RemoveButton onClick={() => handleRemoveRange(index)}>
                🗑
              </RemoveButton>
            )}
          </DateRangeRow>
        ))}

        <AddButton onClick={handleAddRange}>+ Add Date Range</AddButton>

        <ConfirmButton onClick={handleSubmit} disabled={!formValid}>
          Confirm
        </ConfirmButton>
        <CloseButton onClick={onClose}>Cancel</CloseButton>
      </ModalContainer>
    </ModalOverlay>
  );
};

export default NewAnalysisScreen;
