import pytest
import sys
import os
import json
from dotenv import load_dotenv  # 🔹 Importação do dotenv

# 🔹 Garantir que as variáveis do ambiente sejam carregadas
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env')))

# 🔹 Adiciona o diretório raiz ao sys.path para que os módulos sejam encontrados corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ai_services.agents.cluster_evaluator import evaluate_clusters

# 🔹 Simulação dos clusters para teste
mock_clusters = {
    "clusters": {
        "0": [
            "Eu boto fé que as caixas maiores de Switch 2 são reais pois a Nintendo costuma fazer isso mesmo...",
            "Acho que os jogos de Switch que não serão compatíveis nos 2 serão apenas os que usam a câmera do controle...",
            "A regra é clara: Esperar o Nintendo Switch 3 lançar pra baixar o preço do Switch 1 e comprar 😂"
        ],
        "1": [
            "perdi o foco fiquei só olhando os dois canhões de fumaça na frente deles kkkk",
            "Adoro o canal de vocês, mas que CLICKBAIT safado né!!",
            "O PH tá famoso, acabei de assistir o Combo Infinito e eles citando-o como Leaker já."
        ],
        "2": [
            "Ter suporte nativo a mouse, sem precisar de acessório ou gambiarra, é um ponto de venda muito grande.",
            "Porr@! Manual com ilustrações e informações básicas dos controles igual da época do Super Nintendo! ❤🎉",
            "Os joycons como mouse vão ser muito da hora para jogar Metroid Prime!!"
        ],
        "3": [
            "Uma pena um lazer tao bom, nao ser acessível para muita, mas muita gente no BR.",
            "Se a configuração dele for melhor que a do Steam Deck, chuto aí uns 6 a 7 mil no lançamento.",
            "Aguardando o emulador daqui uns anos kkkk"
        ],
        "4": [
            "Mano, a Nintendo bem que podia fazer um remake do Ocarina e Majora nos moldes de Zeldas mais recentes.",
            "Nenhuma empresa vai perder a chance de relançar seus jogos pra uma nova plataforma a preço cheio e faturar milhões de novo.",
            "Pô será que a Nintendo vai salvar os consoles de novo, porque se hoje é comum a galera ter um console em casa muito se deve a ela."
        ]
    },
    "current_k": 4,
    "topic": "Nintendo Switch 2" 
}

def test_evaluate_clusters():
    """Testa se a função retorna um JSON válido com todas as avaliações dos clusters"""
    result = evaluate_clusters(mock_clusters)

    # 🔹 Exibir no terminal a resposta da OpenAI
    print("\n### OpenAI Response ###")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # 🔹 Verifica se o retorno contém a chave 'clusters'
    assert "clusters" in result, "O JSON de retorno deve conter a chave 'clusters'."

    for cluster_id in mock_clusters["clusters"].keys():
        assert cluster_id in result["clusters"], f"O cluster {cluster_id} não foi processado corretamente."

        cluster_data = result["clusters"][cluster_id]

        # 🔹 Verifica se o JSON retornado contém todas as chaves esperadas
        assert "cluster_id" in cluster_data, f"Cluster {cluster_id} não tem a chave 'cluster_id'."
        assert "pattern_found" in cluster_data, f"Cluster {cluster_id} não tem a chave 'pattern_found'."
        assert "keyword" in cluster_data, f"Cluster {cluster_id} não tem a chave 'keyword'."
        assert "conclusion" in cluster_data, f"Cluster {cluster_id} não tem a chave 'conclusion'."
        assert "is_consistent" in cluster_data, f"Cluster {cluster_id} não tem a chave 'is_consistent'."
        assert "topic" in cluster_data, f"Cluster {cluster_id} não tem a chave 'topic'."  # 🔹 Agora verificamos o tema

        # 🔹 Verifica se o cluster_id é o mesmo que foi enviado
        assert str(cluster_data["cluster_id"]) == cluster_id, f"O ID do cluster {cluster_id} não corresponde."

        # 🔹 Verifica se a palavra-chave não está vazia
        assert isinstance(cluster_data["keyword"], str) and cluster_data["keyword"], f"O cluster {cluster_id} retornou uma palavra-chave inválida."

        # 🔹 Verifica se 'is_consistent' é um booleano
        assert isinstance(cluster_data["is_consistent"], bool), f"O cluster {cluster_id} deve retornar um booleano em 'is_consistent'."

if __name__ == "__main__":
    pytest.main()