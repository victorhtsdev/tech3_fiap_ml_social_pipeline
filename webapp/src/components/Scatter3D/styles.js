import styled from "styled-components";

export const ScatterWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  padding: 20px;
  width: 100%;
  max-width: 1000px;
  overflow: hidden; /* 🔥 Evita scroll extra */
`;

export const ScatterContainer = styled.div`
  width: 100%;
  max-width: 800px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden; /* 🔥 Evita que o Plotly ultrapasse os limites */
`;

export const HighlightCard = styled.div`
  width: 35%;
  max-width: 400px;
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
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
  margin-left: auto;
  margin-right: auto;
  max-width: 800px;
`;
