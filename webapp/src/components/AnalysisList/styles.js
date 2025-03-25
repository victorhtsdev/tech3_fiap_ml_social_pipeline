import styled, { keyframes } from "styled-components";

const slideUp = keyframes`
  0% {
    transform: translateY(30px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
`;

// Wrapper Responsivo para os itens de análise e PipelineStatus
export const ResponsiveWrapper = styled.div`
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  gap: 24px;

  @media (max-width: 1024px) {
    flex-direction: column;
    align-items: center;
  }
`;

export const AnalysisContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start; 
  width: 100%;
  max-width: 600px;
  margin-top: 25px;
  gap: 16px;

  @media (max-width: 1024px) {
    align-items: center;
  }
`;

export const AnalysisCard = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  padding: 14px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
  opacity: 0;
  animation: ${slideUp} 0.5s ease-out forwards;

  &:hover {
    background: #f5f5f5;
  }

  &.active {
    background: #e3e3e3;
    color: rgb(58, 91, 237);
    font-weight: bold;
  }
`;

// Wrapper do PipelineStatus para garantir que ele fique centralizado
export const PipelineWrapper = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  min-width: 400px;

  @media (max-width: 1024px) {
    min-width: 100%;
    padding: 10px;
  }
`;

export const AnalysisContent = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
`;

export const AnalysisTitle = styled.h3`
  font-size: 16px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
`;

export const AnalysisDetails = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  font-size: 13px;
  color: #333;
  margin-top: 6px;
`;

export const AnalysisLabel = styled.span`
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  display: flex;
  align-items: center;
`;

export const AnalysisDate = styled.p`
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
`;

export const AnalysisRanges = styled.p`
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
`;

