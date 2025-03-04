import openai
import os
import json
from dotenv import load_dotenv
from openai import OpenAIError  

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_LANGUAGE = os.getenv("LANGUAGE", "pt").strip().lower()  
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o").strip()
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0")) 

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

client = openai.Client(api_key=OPENAI_API_KEY)

def generate_prompt(clusters, current_k, language, topic):
 
    if language not in ["en", "pt"]:
        language = "pt"

    cluster_texts = []
    for cluster_id, comments in clusters.items():
        examples = "\n".join([f"- {comment}" for comment in comments[:50]])  
        cluster_texts.append(f"Cluster {cluster_id}:\n{examples}")

    clusters_text = "\n\n".join(cluster_texts)

    if language == "en":
        prompt = f"""
        You are an AI assistant specialized in analyzing social media comment clusters. The comments were collected based on the topic: **{topic}**.
        The clustering was performed with k={current_k}.

        Below are the clusters and examples of comments:

        {clusters_text}

        Your task:
        1. Identify and describe the **main themes or patterns** in each cluster.
        2. Generate a **SINGLE-WORD KEYWORD** (strictly ONE WORD, written in UPPERCASE) that represents each cluster, ensuring each keyword is UNIQUE within this dataset.
        3. Determine whether the clustering **makes sense** or if any clusters contain **mixed themes**.
        4. If the clustering **is consistent**, the description should be direct and assertive.
        5. If the clustering **is inconsistent or mixed**, indicate that the theme is unclear by using wording like "seems to be related to...".
        6. Return the result strictly in JSON format (no markdown formatting), ensuring each keyword is exactly one word.

        Expected output:

        {{
            "clusters": {{
                "<cluster_id>": {{
                    "cluster_id": <cluster_id>,
                    "topic": "{topic}",
                    "pattern_found": "<concise description of the themes discussed. Avoid uncertainty unless the cluster is mixed>",
                    "keyword": "<unique single-word keyword>",
                    "conclusion": "<does this clustering make sense?>",
                    "is_consistent": <true or false>
                }},
                ...
            }}
        }}
        """
    else:
        prompt = f"""
        Você é um assistente de IA especializado em analisar clusters de comentários de redes sociais. Esses comentários foram coletados com base no tema: **{topic}**.
        O agrupamento foi feito com k={current_k}.

        Abaixo estão os clusters e exemplos de comentários:

        {clusters_text}

        Sua tarefa:
        1. Identificar e descrever os **principais temas ou padrões** presentes em cada cluster.
        2. Gerar uma **PALAVRA-CHAVE ÚNICA** (apenas UMA PALAVRA, escrita em LETRAS MAIÚSCULAS) que representa cada cluster, garantindo que cada palavra-chave seja **diferente das demais**.
        3. Determinar se o agrupamento **faz sentido** ou se há **mistura de temas diferentes**.
        4. Se o agrupamento **for consistente**, a descrição deve ser direta e objetiva.
        5. Se o agrupamento **for inconsistente ou misto**, indique que o tema não é claro usando expressões como "parece estar relacionado a...".
        6. Retornar o resultado estritamente no formato JSON (sem formatação markdown), garantindo que cada palavra-chave tenha **exatamente uma palavra**.

        Formato esperado:

        {{
            "clusters": {{
                "<cluster_id>": {{
                    "cluster_id": <cluster_id>,
                    "topic": "{topic}",
                    "pattern_found": "<descrição objetiva dos temas discutidos. Evite incerteza, a menos que o cluster seja misto>",
                    "keyword": "<uma única palavra única>",
                    "conclusion": "<este agrupamento faz sentido?>",
                    "is_consistent": <true ou false>
                }},
                ...
            }}
        }}
        """

    return prompt.strip()

def evaluate_clusters(clusters_json):
    """
    Recebe um JSON contendo os clusters e seus comentários,
    chama o LLM para avaliar todos os clusters de uma vez e retorna um JSON consolidado.
    """
    if not isinstance(clusters_json, dict) or "clusters" not in clusters_json or "current_k" not in clusters_json or "topic" not in clusters_json:
        raise ValueError("Formato inválido. Esperado {'clusters': {cluster_id: [comments]}, 'current_k': k_value, 'topic': 'search_topic'}")

    clusters = clusters_json["clusters"]
    current_k = clusters_json["current_k"]
    topic = clusters_json["topic"]  # 🔹 Tema da busca

    prompt = generate_prompt(clusters, current_k, AGENT_LANGUAGE, topic)

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Você avalia a coerência de clusters e responde estritamente no formato JSON, sem formatação markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMPERATURE
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```json"):
            content = content[7:-3].strip()

        result = json.loads(content)

        used_keywords = set()
        for cluster_id, cluster_data in result["clusters"].items():
            keyword = cluster_data["keyword"].split()[0]
            attempt = 1

            while keyword in used_keywords:
                print(f"🔄 Palavra-chave '{keyword}' já usada. Tentando outra... (Tentativa {attempt})")
                prompt = generate_prompt(clusters, current_k, AGENT_LANGUAGE, topic)  
                response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "Gere palavras-chave únicas para cada cluster."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=OPENAI_TEMPERATURE
                )

                content = response.choices[0].message.content.strip()
                result = json.loads(content)
                keyword = result["clusters"][cluster_id]["keyword"].split()[0]
                attempt += 1

            used_keywords.add(keyword)
            result["clusters"][cluster_id]["keyword"] = keyword 

        return result

    except json.JSONDecodeError:
        raise ValueError(f"Erro no JSON recebido da OpenAI: {content}")

    except OpenAIError as e:
        raise RuntimeError(f"Erro na API OpenAI: {str(e)}")

    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {str(e)}")
