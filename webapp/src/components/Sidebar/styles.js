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

export const SidebarContainer = styled.div`
  width: 240px;
  height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #ddd;
  position: fixed;
  top: 0;
  left: 0;
  overflow: hidden;
  z-index: 20;
`;

export const SearchBarWrapper = styled.div`
  padding: 16px;
`;

export const SidebarDivider = styled.div`
  width: 100%;
  height: 1px;
  background: #ddd;
`;

export const SearchBar = styled.div`
  display: flex;
  align-items: center;
  background: white;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ddd;
  position: relative;

  input {
    border: none;
    outline: none;
    margin-left: 8px;
    width: 100%;
    padding: 6px;
    font-size: 14px;
    border-radius: 4px;
    background: white;
    color: #333;
  }

  input::placeholder {
    color: #aaa;
  }

  svg {
    color: #666;
  }
`;

export const Divider = styled.div`
  width: 100%;
  height: 1px;
  background: #ddd;
  margin-top: 8px; /* Garante espaçamento adequado */
  margin-bottom: 8px;
`;

export const MenuWrapper = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 0 16px 16px 16px;
`;

export const MenuItem = styled.div`
  display: flex;
  align-items: center;
  padding: 14px;
  margin-bottom: 8px;
  gap: 10px;
  cursor: pointer;
  font-size: 16px;
  color: #333;
  border-radius: 8px;
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
