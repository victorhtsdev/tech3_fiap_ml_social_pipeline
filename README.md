# Análise de Comentários do YouTube com LLM e Machine Learning

Este projeto foi desenvolvido como parte do curso de pós-graduação em Machine Learning Engineering da FIAP, no contexto do Tech Challenge da fase voltada a MLOps. O objetivo foi projetar e implementar um pipeline de coleta, processamento e análise de dados de forma automatizada, integrando diferentes tecnologias e técnicas de aprendizado de máquina.

## Visão Geral do Projeto

A proposta consiste em coletar comentários do YouTube relacionados a termos de busca definidos pelo usuário, rotular automaticamente esses comentários utilizando um modelo de linguagem (LLM), gerar embeddings com a API da OpenAI e treinar modelos supervisionados (SVM e XGBoost) para classificação. O projeto também conta com uma aplicação web que permite realizar novas análises com base em modelos já treinados e visualizar os resultados por meio de gráficos interativos.

## Estrutura do Projeto

. ├── backend/ # API Flask para orquestração e análise ├── frontend/ # Aplicação React para visualização ├── notebooks/ # Notebooks de experimentação e treino ├── data/ # Armazenamento local de dados (opcional) ├── models/ # Modelos treinados e versionados ├── requirements.txt # Dependências ├── README.md # Documentação do projeto └── docker/ # Arquivos de configuração do ambiente

markdown
Copy
Edit

## Tecnologias Utilizadas

- Python (Flask, pandas, scikit-learn, SQLAlchemy)
- React (com Axios, Plotly para visualizações)
- OpenAI API (para embeddings)
- DeepSeek LLM (para rotulagem automática)
- YouTube Data API v3
- PostgreSQL (armazenamento dos dados)
- Docker (opcional, para deploy local)
- AWS EC2 (para hospedagem da aplicação)
- AWS RDS (PostgreSQL gerenciado na nuvem)

## Etapas da Solução

1. **Coleta de Comentários**: o usuário insere um termo de busca, intervalo de datas e seleciona um modelo para análise. A API do YouTube é usada para coletar vídeos e comentários.
2. **Rotulagem com LLM**: os comentários são enviados para um modelo de linguagem (DeepSeek) que retorna categorias sugeridas.
3. **Geração de Embeddings**: os textos rotulados são vetorizados com a API de embeddings da OpenAI.
4. **Treinamento Supervisionado**: com os dados vetorizados, os modelos SVM e XGBoost são treinados e avaliados.
5. **Aplicação Web**: permite a realização de novas buscas, a seleção de modelos treinados e a visualização interativa dos resultados.

## Funcionalidades da Aplicação

- Busca de vídeos e coleta de comentários diretamente da interface
- Escolha do modelo treinado para aplicar em novas análises
- Exibição de gráficos como:
  - Distribuição de categorias
  - Gráfico de série temporal
  - Projeção 3D dos embeddings
  - Comparação entre modelos
