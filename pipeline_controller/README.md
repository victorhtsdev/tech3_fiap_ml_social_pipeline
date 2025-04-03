
# Backend - Análise de Comentários do YouTube

Este backend foi desenvolvido em Flask e faz parte do projeto de Análise de Comentários do YouTube com LLM e Machine Learning, os métodos são utilizados pela aplicação frontend.

---

## Autenticação

### Gerar Token
**URL:** `/get_token`  
**Método:** `GET`  
**Descrição:** Gera um token de autenticação fixo para uso nas requisições.  
**Resposta:**
```json
{
  "token": "seu_token_aqui"
}
```

---

## Execução de Pipeline

### Iniciar Pipeline
**URL:** `/run_pipeline`  
**Método:** `POST`  
**Token:** Requerido  
**Descrição:** Inicia o processo de coleta, rotulagem, vetorização e classificação.  
**Parâmetros:**
```json
{
  "search": "string",
  "date_ranges": [{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}],
  "classification_model_version": 1,
  "classification_model_name": "SVM",
  "classification_model_type": "CONSOLE"
}
```
**Respostas:**
- `200 OK`: Pipeline iniciado com sucesso.
```json
{
  "message": "Pipeline started",
  "exec_id": "uuid"
}
```

---

### Verificar Status do Pipeline
**URL:** `/get_pipeline_status?exec_id=<uuid>`  
**Método:** `GET`  
**Token:** Requerido  
**Descrição:** Retorna o status de cada etapa da execução do pipeline.  
**Resposta:**
- `200 OK`  
```json
{
  "execution_id": "uuid",
  "stages": [
    { "name": "Data Collection", "status": "Completed" },
    { "name": "Preprocessing Data", "status": "Completed" },
    { "name": "Embedding Generation", "status": "Completed" },
    { "name": "ML Classification", "status": "Completed" },
    { "name": "Pipeline Execution", "status": "Completed" }
  ]
}
```

---

## Execuções e Modelos

### Última Execução por Termo
**URL:** `/get_ml_execution_last_version`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK` 
```json
[
  {
    "id": "uuid",
    "search": "videogame",
    "date": "2025-03-08T19:47:53",
    "classification_model_version": 1,
    "classification_model_name": "SVM",
    "classification_model_type": "CONSOLE",
    "date_ranges": [...]
  }
]
```

---

### Listar Execuções por Termo
**URL:** `/get_ml_executions_by_search?search=<termo>`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK`  
```json
[
  {
    "id": "uuid",
    "search": "Nintendo Switch 2",
    "date": "2025-03-08T19:47:53",
    "classification_model_version": 1,
    "classification_model_name": "SVM",
    "classification_model_type": "CONSOLE",
    "date_ranges": [...]
  }
]
```

---

### Deletar Execução
**URL:** `/delete_execution?exec_id=<uuid>`  
**Método:** `DELETE`  
**Token:** Requerido  
**Resposta:**
- `200 OK`  
```json
{
  "message": "Data successfully deleted for exec_id: uuid"
}
```

---

## Visualizações e Resultados

### Embeddings
**URL:** `/get_embeddings?exec_id=<uuid>`  
**Método:** `GET`  
**Token:** Requerido  
**Descrição:** Retorna frases, labels, content_id e embeddings reduzidos com PCA.  
**Resposta:**
- `200 OK` 
```json
[
  {
    "sentence": "O desempenho está ótimo",
    "embedding": [0.25, -0.14, ...],
    "label": "Performance",
    "content_id": 123
  }
]
```

### Categorias (SVM)
**URL:** `/get_svm_category_counts?exec_id=<uuid>`  
**Método:** `GET`  
**Token:** Requerido  
**Descrição:** Retorna contagem de rótulos.  
**Resposta:**
- `200 OK` 
```json
[
  { "label": "Desempenho", "count": 15 },
  { "label": "Preço", "count": 8 }
]
```

### Word Cloud
**URL:** `/get_word_cloud?exec_id=<uuid>`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK` 
```json
[
  {
    "label": "Design",
    "words": [
      { "word": "bonito", "count": 12 },
      { "word": "compacto", "count": 8 }
    ]
  }
]
```

### Cores por Categoria
**URL:** `/get_category_colors?exec_id=<uuid>`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK` 
```json
{
  "Design": "#ff5733",
  "Preço": "#33c1ff",
  "Desempenho": "#75ff33"
}
```

### Frases Agrupadas por Comentário Original
**URL:** `/get_sentences_by_label?exec_id=<uuid>&label=<label>`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK` 
```json
[
  {
    "content_id": 301,
    "label": "Design",
    "original_comment": "Achei o design muito bonito e moderno.",
    "sentences": [
      {
        "processed_id": 1,
        "sentence": "Achei o design muito bonito"
      },
      {
        "processed_id": 2,
        "sentence": "e moderno"
      }
    ]
  }
]
```

### Série Temporal por Label
**URL:** `/get_time_series_label?exec_id=<uuid>`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK` 
```json
[
  { "label": "Design", "date": "2025-03-01", "count": 10, "color": "#ff5733" },
  { "label": "Preço", "date": "2025-03-01", "count": 4, "color": "#33c1ff" }
]
```

---

## Métricas

### Obter Métricas dos Modelos
**URL:** `/get_model_metrics`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK` 
```json
{
  "CONSOLE": {
    "1": [
      {
        "model_id": "uuid",
        "model_name": "SVM",
        "is_recommended": true,
        "global_metrics": {
          "accuracy": 0.89,
          "macro_f1": 0.84,
          "weighted_f1": 0.87
        },
        "class_metrics": [
          { "class_name": "Design", "f1_score": 0.82 },
          { "class_name": "Preço", "f1_score": 0.85 }
        ]
      }
    ]
  }
}
```

### Obter Modelos Disponíveis
**URL:** `/get_models`  
**Método:** `GET`  
**Token:** Requerido  
**Resposta:**
- `200 OK` 
```json
{
  "types": ["CONSOLE", "SMARTPHONE"],
  "models": {
    "CONSOLE": [
      {
        "id": "uuid",
        "label": "SVM - v1"
      },
      {
        "id": "uuid2",
        "label": "XGBOOST - v1"
      }
    ]
  }
}
```

---

## Observações

- Todos os endpoints protegidos requerem um token JWT no header:  
  `Authorization: Bearer <seu_token>`

- O pipeline é assíncrono: a análise é iniciada em segundo plano e pode ser acompanhada pelo status.

- A autenticação foi implementada de forma simplificada e está sujeita a melhorias em versões futuras.

---

## Requisitos

```
flask==3.0.3
sqlalchemy==2.0.40
psycopg2-binary==2.9.10
pandas==2.2.3
numpy==2.2.4
scikit-learn==1.6.1
nltk==3.9.1
openai==1.69.0
ollama==0.4.7
python-dotenv==1.1.0
emoji==2.14.1
requests==2.32.3
pyjwt==2.10.1
flask-cors==5.0.1
xgboost==3.0.0
```
