import styled from "styled-components";

export const TableContainer = styled.div`
  margin-top: 40px;
  width: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  padding: 0 20px;
`;

export const SectionTitle = styled.h2`
  font-size: 20px;
  margin-bottom: 4px;
  text-align: left;
  width: 100%;
`;

export const SectionDescription = styled.p`
  margin-bottom: 20px;
  color: #555;
  text-align: left;
  width: 100%;
`;

export const TableHeader = styled.div`
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  width: 100%;
`;

export const SelectFilter = styled.select`
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  min-width: 200px;
  max-width: 100%;
`;

export const ScrollableTable = styled.div`
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 6px;
  width: 100%;
  box-sizing: border-box;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
  }
`;

export const TableRow = styled.div`
  display: flex;
  flex-direction: column;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-bottom: 16px;
  width: 100%;
  box-sizing: border-box;
  
  @media (min-width: 768px) {
    flex-direction: row;
  }
`;

export const CommentCell = styled.div`
  width: 100%;
  background: #f9f9f9;
  padding: 12px;
  border-bottom: 1px solid #ddd;
  box-sizing: border-box;
  word-break: break-word;

  @media (min-width: 768px) {
    width: 40%;
    border-bottom: none;
    border-right: 1px solid #ddd;
  }
`;

export const SentencesCell = styled.div`
  width: 100%;
  padding: 12px;
  background: #fff;
  box-sizing: border-box;
  word-break: break-word;

  @media (min-width: 768px) {
    width: 60%;
  }

  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
    width: 100%;
    box-sizing: border-box;

    @media (min-width: 480px) {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .grid-item {
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 8px;
    border: 1px solid #e0e0e0;
    word-break: break-word;
    box-sizing: border-box;
  }
`;