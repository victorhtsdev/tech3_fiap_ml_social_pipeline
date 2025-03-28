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

export const ModalOverlay = styled.div`
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

export const ModalContainer = styled.div`
  background: white;
  padding: 32px;
  border-radius: 16px;
  width: 420px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  animation: ${slideUp} 0.4s ease-out forwards;
`;

export const ModalTitle = styled.h2`
  margin-bottom: 24px;
  font-size: 20px;
  color: #333;
  font-weight: bold;
`;

export const FieldGroup = styled.div`
  margin-bottom: 16px;
`;

export const Label = styled.label`
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #444;
`;

export const Select = styled.select`
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border-radius: 8px;
  border: 1px solid #ccc;
  background: #fafafa;
  color: #333;
  transition: border 0.3s;

  &:focus {
    border-color: #4f46e5;
    outline: none;
  }
`;

export const DateInput = styled.input`
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border-radius: 8px;
  border: 1px solid #ccc;
  background: #fafafa;
  color: #333;
  transition: border 0.3s;

  &:focus {
    border-color: #4f46e5;
    outline: none;
  }
`;

export const ConfirmButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: bold;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
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


export const CloseButton = styled(ConfirmButton)`
  background: #f0f0f0;
  color: #333;
  margin-top: 8px;

  &:hover {
    background: #e0e0e0;
  }
`;


export const DateRangeRow = styled.div`
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
`;

export const AddButton = styled.button`
  padding: 8px 12px;
  background: white;
  border: 1px dashed #ccc;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  margin-bottom: 16px;

  &:hover {
    background: #f3f3f3;
  }
`;

export const RemoveButton = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  font-size: 16px;

  &:hover {
    color: #e74c3c;
  }
`;
