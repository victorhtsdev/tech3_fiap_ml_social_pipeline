import React, { useEffect, useState } from "react";
import { getSentencesByLabel } from "../../services/api";
import {
  TableContainer,
  TableHeader,
  SelectFilter,
  TableRow,
  CommentCell,
  SentencesCell,
  ScrollableTable,
  SectionTitle,
  SectionDescription,
} from "./styles";

const ContentTable = ({ execId, categories }) => {
  const [selectedCategory, setSelectedCategory] = useState("");
  const [groupedData, setGroupedData] = useState([]);

  useEffect(() => {
    const fetchSentences = async () => {
      if (!selectedCategory) return;

      try {
        const data = await getSentencesByLabel(execId, selectedCategory);
        setGroupedData(data);
      } catch (error) {
        console.error("Erro ao buscar frases por categoria:", error);
      }
    };

    fetchSentences();
  }, [execId, selectedCategory]);

  return (
    <TableContainer>
      <SectionTitle>Frases por Categoria Selecionada</SectionTitle>
      <SectionDescription>
        Visualize as frases classificadas pelo modelo, agrupadas por comentário original.
      </SectionDescription>

      <TableHeader>
        <label htmlFor="category-select"><strong>Filtrar por categoria:</strong></label>
        <SelectFilter
          id="category-select"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="">Selecione...</option>
          {categories.map((c) => (
            <option key={c.label} value={c.label}>
              {c.label}
            </option>
          ))}
        </SelectFilter>
      </TableHeader>

      <ScrollableTable>
        {groupedData.length > 0 && (
          <TableRow>
            <CommentCell><strong>Comentário Original</strong></CommentCell>
            <SentencesCell><strong>Frases</strong></SentencesCell>
          </TableRow>
        )}

        {groupedData.map((item) => (
          <TableRow key={item.content_id}>
            <CommentCell>{item.original_comment}</CommentCell>
            <SentencesCell>
              <div className="grid">
                {item.sentences.map((s) => (
                  <div key={s.processed_id} className="grid-item">
                    {s.sentence}
                  </div>
                ))}
              </div>
            </SentencesCell>
          </TableRow>
        ))}
      </ScrollableTable>
    </TableContainer>
  );
};

export default ContentTable;
