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

export const Wrapper = styled.div`
  width: 100%;
  text-align: center;
`;

export const CardContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  width: 100%;
  padding: 15px;
`;

export const Card = styled.div`
  background: white;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 10px;
  width: 260px;
  height: 200px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  animation: ${slideUp} 0.5s ease-out forwards;
  overflow: hidden;

  &:hover {
    transform: scale(1.02);
  }
`;

export const CardTitle = styled.h3`
  font-size: 16px;
  text-align: center;
  margin-bottom: 5px;
  color: #2563eb;
`;

export const ScrollableTable = styled.div`
  max-height: 140px;
  overflow-y: auto;
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

export const Th = styled.th`
  background: #f3f4f6;
  padding: 6px;
  font-size: 12px;
  text-align: left;
  border-bottom: 2px solid #d1d5db;
`;

export const Td = styled.td`
  padding: 5px;
  font-size: 12px;
  border-bottom: 1px solid #d1d5db;
`;

export const ChartTitle = styled.h2`
  font-size: 20px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-bottom: 5px;
`;

export const ChartDescription = styled.p`
  font-size: 14px;
  color: #666;
  text-align: center;
  margin-bottom: 15px;
`;
