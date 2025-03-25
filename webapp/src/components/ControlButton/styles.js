import styled from "styled-components";

export const ButtonContainer = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s, color 0.3s, border 0.3s;

  &:hover {
    background: #f3f3f3;
  }

  &:disabled {
    color: #bbb;
    border-color: #eee;
    cursor: not-allowed;
    background: #f9f9f9;
  }
`;
