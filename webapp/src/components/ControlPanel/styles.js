import styled from "styled-components";

export const ControlPanelContainer = styled.div`
  width: calc(100% - 240px);
  height: 86px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px; 
  padding: 0 20px;
  background: white;
  border-bottom: 1px solid #ddd;
  position: fixed;
  top: 0;
  left: 240px;
  right: 0;
  overflow: hidden;
  z-index: 5;
`;


export const ControlPanelDivider = styled.div`
  width: 100%;
  height: 1px;
  background: #ddd;
  position: absolute;
  bottom: 0;
  left: 0;
`;
