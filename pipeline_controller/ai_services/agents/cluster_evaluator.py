import openai
import os
import json
from dotenv import load_dotenv
from openai import OpenAIError  # 🔹 Importação correta para capturar erros

# 🔹 Carregar variáveis do .env
load_dotenv()

# 🔹 Definir variáveis globais do ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_LANGUAGE = os.getenv("AGENT_LANGUAGE", "en").strip().lower()  # Default "en"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o").strip()
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0"))  # Convertendo para float

# 🔹 Validar a chave da API no início
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

# 🔹 Criar cliente OpenAI corretamente
client = openai.Client(api_key=OPENAI_API_KEY)

def generate_prompt(cluster_id, comments, current_k, language, topic):
    """Gera o prompt para avaliação de um cluster, considerando o tema geral da busca na rede social."""
    if language not in ["en", "pt"]:
        language = "en"

    examples = "\n".join([f"- {comment}" for comment in comments[:5]])

    if language == "en":
        prompt = f"""
        You are an AI assistant specialized in analyzing clusters of social media comments. These comments were collected based on the topic: **{topic}**.
        The clustering was performed with k={current_k}.

        Below is a sample of comments grouped together in cluster {cluster_id}:

        {examples}

        Your task is:
        1. Identify and describe the **main themes or patterns** within this cluster.
        2. Generate a **single keyword** (one word only) that represents this cluster, making it easy to label (e.g., "Price", "Gameplay", "Hardware").
        3. Determine if the clustering **makes sense** or if the cluster contains **mixed themes**.
        4. Return the result in the following JSON format (no markdown or code block formatting):

        {{
            "cluster_id": {cluster_id},
            "topic": "{topic}",
            "pattern_found": "<brief description of the themes discussed>",
            "keyword": "<single word that represents the cluster>",
            "conclusion": "<does this clustering make sense?>",
            "is_consistent": <true or false>
        }}
        """
    else:
        prompt = f"""
        Você é um assistente de IA especializado em analisar clusters de comentários de redes sociais. Esses comentários foram coletados com base no tema: **{topic}**.
        O agrupamento foi feito com k={current_k}.

        Abaixo está um exemplo de comentários agrupados no cluster {cluster_id}:

        {examples}

        Sua tarefa é:
        1. Identificar e descrever os **principais temas ou padrões** presentes neste cluster.
        2. Gerar uma **palavra-chave única** (apenas uma palavra) que representa este cluster, facilitando a nomeação (ex.: "Preço", "Hardware", "Jogabilidade").
        3. Determinar se o agrupamento **faz sentido** ou se há **mistura de temas diferentes**.
        4. Retornar o resultado no seguinte formato JSON (sem markdown ou formatação de bloco de código):

        {{
            "cluster_id": {cluster_id},
            "topic": "{topic}",
            "pattern_found": "<descrição breve dos temas discutidos>",
            "keyword": "<uma única palavra que representa o cluster>",
            "conclusion": "<este agrupamento faz sentido?>",
            "is_consistent": <true ou false>
        }}
        """
    return prompt.strip()


def evaluate_clusters(clusters_json):
    """
    Recebe um JSON contendo os clusters e seus comentários,
    chama o LLM para avaliar cada cluster e retorna um JSON consolidado.
    """
    if not isinstance(clusters_json, dict) or "clusters" not in clusters_json or "current_k" not in clusters_json or "topic" not in clusters_json:
        raise ValueError("Invalid JSON format. Expected {'clusters': {cluster_id: [comments]}, 'current_k': k_value, 'topic': 'search_topic'}")

    clusters = clusters_json["clusters"]
    current_k = clusters_json["current_k"]
    topic = clusters_json["topic"]  # 🔹 Parâmetro do tema da busca

    results = {}

    for cluster_id, comments in clusters.items():
        prompt = generate_prompt(cluster_id, comments, current_k, AGENT_LANGUAGE, topic)

        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You evaluate the coherence of clusters and respond strictly in JSON format, without markdown formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE
            )

            content = response.choices[0].message.content.strip()

            # 🔹 Se a resposta vier formatada como ```json ... ```, removemos os delimitadores
            if content.startswith("```json"):
                content = content[7:-3].strip()

            results[cluster_id] = json.loads(content)

        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON response from OpenAI for cluster {cluster_id}: {content}")

        except OpenAIError as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")

    return {"clusters": results}
