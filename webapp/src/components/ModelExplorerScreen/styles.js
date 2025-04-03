import styled from "styled-components";

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

export const SelectStyled = styled.select`
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 14px;
  color: #374151;
  font-weight: 500;
  cursor: pointer;

  &:hover {
    background: #e5e7eb;
  }

  &:focus {
    outline: none;
    border-color: #a3a3a3;
  }
`;

export const FilterContainer = styled.div`
  margin-bottom: 16px;
  display: flex;
  gap: 16px;
  align-items: center;
`;
