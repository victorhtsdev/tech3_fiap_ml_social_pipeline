import styled from "styled-components";

export const TableContainer = styled.div`
  margin-top: 40px;
  width: 100%;
  text-align: left;
`;

export const SectionTitle = styled.h2`
  font-size: 20px;
  margin-bottom: 4px;
  text-align: left;
`;

export const SectionDescription = styled.p`
  margin-bottom: 20px;
  color: #555;
  text-align: left;
`;

export const TableHeader = styled.div`
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
`;

export const SelectFilter = styled.select`
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
`;

export const ScrollableTable = styled.div`
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 8px;
`;

export const TableRow = styled.div`
  display: flex;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-bottom: 16px;
  overflow: hidden;
`;

export const CommentCell = styled.div`
  flex: 1;
  background: #f9f9f9;
  padding: 12px;
  border-right: 1px solid #ddd;
  text-align: left;
`;

export const SentencesCell = styled.div`
  flex: 1.5;
  padding: 12px;
  background: #fff;
  text-align: left;

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 8px;
  }

  .grid-item {
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 8px;
    border: 1px solid #e0e0e0;
  }
`;
