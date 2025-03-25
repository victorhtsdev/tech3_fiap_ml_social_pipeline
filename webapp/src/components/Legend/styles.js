import styled from "styled-components";

export const LegendContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  background: white;
  padding: 10px;
  width: 100%;
  max-width: 1200px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
`;

export const LegendItem = styled.button`
  border: none;
  cursor: pointer;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: bold;
  border-radius: 6px;
  transition: all 0.3s ease;
  color: white;
  background-color: ${({ active }) => (active ? "#007BFF" : "#ccc")};
  opacity: ${({ active }) => (active ? 1 : 0.5)};
  text-align: center;
  white-space: nowrap;

  &:hover {
    opacity: 0.8;
  }
`;
