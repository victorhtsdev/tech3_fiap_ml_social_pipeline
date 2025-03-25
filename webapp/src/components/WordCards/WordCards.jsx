import React from "react";
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
  Wrapper
} from "./styles";

const WordCards = ({ data, hiddenCategories }) => {
  return (
    <Wrapper>
      {/* 🔹 Título e descrição separados do CardContainer */}
      <ChartTitle>Distribuição de Palavras por Categoria</ChartTitle>
      <ChartDescription>
        Este painel exibe as palavras mais frequentes dentro de cada categoria detectada pelo modelo de machine learning.
      </ChartDescription>

      <CardContainer>
        {/* 🔹 Renderiza os cards */}
        {Object.entries(data).map(([category, words]) => (
          !hiddenCategories.has(category) && ( 
            <Card key={category}>
              <CardTitle>{category}</CardTitle>
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
          )
        ))}
      </CardContainer>
    </Wrapper>
  );
};

export default WordCards;
