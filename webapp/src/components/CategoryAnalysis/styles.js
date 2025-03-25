import styled from "styled-components";

export const CategoryAnalysisContainer = styled.div`
  width: 100%;
  max-width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  overflow: hidden;
  box-sizing: border-box;
  min-height: 100vh;
  position: relative;
`;

export const ChartContainer = styled.div`
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  overflow-x: hidden;
`;

export const BackButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: bold;
  color: #374151;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
  
  &:hover {
    background: #e5e7eb;
  }
`;
