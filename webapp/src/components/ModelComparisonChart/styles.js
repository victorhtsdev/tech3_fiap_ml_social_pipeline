import styled from "styled-components";

export const ChartContainer = styled.div`
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
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

export const ChartExplanation = styled.div`
  font-size: 14px;
  color: #444;
  max-width: 900px;
  margin: 0 auto 20px auto;
  line-height: 1.6;
  text-align: center;

  strong {
    font-weight: 600;
  }
`;

export const ChartNote = styled.div`
  margin-top: 24px;
  font-size: 15px;
  font-weight: 600;
  color: #222;
  text-align: center;
`;