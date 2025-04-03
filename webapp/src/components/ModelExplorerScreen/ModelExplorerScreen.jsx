import React, { useEffect, useState } from "react";
import { getModelMetrics } from "../../services/api";
import { BackButton, SelectStyled, FilterContainer } from "./styles";
import ModelComparisonChart from "../ModelComparisonChart/ModelComparisonChart";
import ClassComparisonChart from "../ClassComparisonChart/ClassComparisonChart";

const ModelExplorerScreen = ({ onBack }) => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedType, setSelectedType] = useState("");
  const [selectedVersion, setSelectedVersion] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const result = await getModelMetrics();
      setData(result);

      const types = Object.keys(result);
      if (types.length > 0) {
        setSelectedType(types[0]);
        const firstVersion = Object.keys(result[types[0]])[0];
        setSelectedVersion(firstVersion);
      }

      setLoading(false);
    };

    fetchData();
  }, []);

  const versions = selectedType ? Object.keys(data[selectedType] || {}) : [];

  return (
    <div style={{ padding: "20px" }}>
      <FilterContainer>
        <BackButton onClick={onBack}>← Back</BackButton>

        <SelectStyled
          value={selectedType}
          onChange={(e) => setSelectedType(e.target.value)}
        >
          {Object.keys(data).map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </SelectStyled>

        <SelectStyled
          value={selectedVersion}
          onChange={(e) => setSelectedVersion(e.target.value)}
        >
          {versions.map((v) => (
            <option key={v} value={v}>
              v{v}
            </option>
          ))}
        </SelectStyled>
      </FilterContainer>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <ModelComparisonChart
            data={data[selectedType]?.[selectedVersion] || []}
          />

          <ClassComparisonChart
            data={data[selectedType]?.[selectedVersion] || []}
          />

          <div
            style={{
              maxWidth: "900px",
              margin: "40px auto 0 auto",
              padding: "20px",
              background: "#f9fafb",
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
            }}
          >
            <h2
              style={{
                fontSize: "20px",
                fontWeight: "bold",
                color: "#1f2937",
                marginBottom: "16px",
              }}
            >
              Escolha do Modelo
            </h2>

            <p
              style={{
                fontSize: "15px",
                color: "#374151",
                lineHeight: "1.6",
                marginBottom: "12px",
              }}
            >
              Após análise comparativa entre os modelos <strong>SVM</strong> e{" "}
              <strong>XGBoost</strong>, foi observado que o
              <strong style={{ color: "#059669" }}> ✔️ SVM</strong> apresentou
              melhor desempenho geral nas métricas de F1-score. Além disso, foi
              constatada uma consistência superior em diversas classes,
              especialmente nas categorias mais representativas, sendo assim
              definido como o modelo recomendado <strong>neste momento</strong>.
            </p>

            <p
              style={{
                fontSize: "15px",
                color: "#374151",
                lineHeight: "1.6",
                marginBottom: "12px",
              }}
            >
              O desempenho computacional também foi semelhante entre os modelos:
              tanto o tempo de treino quanto o tempo de geração das previsões
              ficaram em níveis parecidos, sem impacto significativo na escolha
              final. No entanto, foi percebido que, à medida que o volume de
              dados aumenta, o tempo de treinamento do <strong>SVM</strong>{" "}
              tende a crescer mais rapidamente em comparação ao{" "}
              <strong>XGBoost</strong>, além disso o modelo <strong>SVM</strong>
              {" "}ocupa um espaço muito maior em disco, como há somente 2 tipos de 
              treinamento de modelo na aplicação GAME_CONSOLE e SMARTPHONE o 
              espaço em disco ocupado ainda é viável, mas caso existam mais tipos
              o <strong>SVM</strong> pode se tornar inviável.
            </p>

            <h3
              style={{
                fontSize: "17px",
                fontWeight: "bold",
                color: "#1f2937",
                marginTop: "24px",
                marginBottom: "8px",
              }}
            >
              Representação Textual com Embeddings
            </h3>
            <p
              style={{
                fontSize: "15px",
                color: "#374151",
                lineHeight: "1.6",
                marginBottom: "12px",
              }}
            >
              Modelos modernos de embeddings, como o{" "}
              <strong>text-embedding-3-large</strong>, processam todas as
              palavras de uma frase — incluindo as <i>stop words</i> — e
              aprendem automaticamente quais termos são mais relevantes para a
              construção do significado. Essas palavras funcionam como
              conectores contextuais e ajudam o modelo a entender as relações
              entre os termos principais.
            </p>
            <p
              style={{
                fontSize: "15px",
                color: "#374151",
                lineHeight: "1.6",
                marginBottom: "12px",
              }}
            >
              Como SVM e XGBoost operam sobre os vetores gerados pelos
              embeddings, e não sobre as palavras diretamente, a presença de
              stop words na entrada textual não compromete o desempenho. Na
              prática, a remoção dessas palavras pode até enfraquecer a
              representação semântica da frase, prejudicando o aprendizado dos
              padrões.
            </p>

            <h3
              style={{
                fontSize: "17px",
                fontWeight: "bold",
                color: "#1f2937",
                marginTop: "24px",
                marginBottom: "8px",
              }}
            >
              Potencial de Aprimoramento do XGBoost
            </h3>
            <p
              style={{
                fontSize: "15px",
                color: "#374151",
                lineHeight: "1.6",
                marginBottom: "12px",
              }}
            >
              O modelo <strong>XGBoost</strong> possui muitos hiperparâmetros
              que ainda não foram explorados neste trabalho. Com mais testes e
              ajustes, há potencial para que ele supere o SVM em versões
              futuras.
            </p>

            <h3
              style={{
                fontSize: "17px",
                fontWeight: "bold",
                color: "#1f2937",
                marginTop: "24px",
                marginBottom: "8px",
              }}
            >
              Recomendações para novas versões
            </h3>
            <ul
              style={{
                fontSize: "15px",
                color: "#374151",
                lineHeight: "1.8",
                paddingLeft: "20px",
                marginBottom: "12px",
              }}
            >
              <li>
                Investigar diferentes técnicas de balanceamento de classes.
              </li>
              <li>Aumentar o volume de dados de treino.</li>
              <li>Testar o XGBoost com outros parâmetros.</li>
              <li>
                Avaliar e alterar os rótulos, principalmente aqueles que pontuam
                pouco.
              </li>
              <li>Testar outros modelos, como, por exemplo, redes neurais.</li>
            </ul>
          </div>
        </>
      )}
    </div>
  );
};

export default ModelExplorerScreen;
