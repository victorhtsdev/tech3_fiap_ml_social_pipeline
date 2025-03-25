import styled from "styled-components";

export const ChartContainer = styled.div`
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  overflow-x: hidden; /* Evita rolagem lateral */
  box-sizing: border-box;
`;

export const ChartTitle = styled.h2`
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
`;

export const ChartDescription = styled.p`
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
`;
