import React, { useState } from "react";
import { 
  CardContainer, 
  Card, 
  CardTitle, 
  ScrollableTable, 
  Table, 
  Th, 
  Td, 
  ChartTitle, 
  ChartDescription,
  Wrapper,
  ExpandButton
} from "./styles";

const WordCards = ({ data, hiddenCategories }) => {
  const [showAll, setShowAll] = useState(false);

  const normalizedData = Array.isArray(data)
    ? data
    : Object.entries(data).map(([label, words]) => ({ label, words }));

  const visibleData = normalizedData.filter(({ label }) => !hiddenCategories.has(label));
  const cardsPerLine = 3;
  const maxVisibleCards = cardsPerLine * 2;
  const displayedCards = showAll ? visibleData : visibleData.slice(0, maxVisibleCards);

  return (
    <Wrapper>
      <ChartTitle>Distribuição de Palavras por Categoria</ChartTitle>
      <ChartDescription>
        Este painel exibe as palavras mais frequentes dentro de cada categoria detectada pelo modelo de machine learning.
      </ChartDescription>

      <CardContainer>
        {displayedCards.map(({ label, words }) => (
          <Card key={label}>
            <CardTitle>{label}</CardTitle>
            <ScrollableTable>
              <Table>
                <thead>
                  <tr>
                    <Th>Palavra</Th>
                    <Th>Frequência</Th>
                  </tr>
                </thead>
                <tbody>
                  {words.map(({ word, count }) => (
                    <tr key={word}>
                      <Td>{word}</Td>
                      <Td>{count}</Td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </ScrollableTable>
          </Card>
        ))}
      </CardContainer>

      {visibleData.length > maxVisibleCards && (
        <ExpandButton onClick={() => setShowAll(!showAll)}>
          {showAll ? "Ver menos ▲" : "Ver mais ▼"}
        </ExpandButton>
      )}
    </Wrapper>
  );
};

export default WordCards;
