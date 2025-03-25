from enum import Enum

class GameConsoleCategoryColors(Enum):
    VENDAS = "#1f77b4"
    JOGOS = "#ff7f0e"
    EXPECTATIVA_DE_COMPRA = "#2ca02c"
    PRECO = "#d62728"
    RUMORES_E_VAZAMENTOS = "#9467bd"
    PERIFERICOS_E_ACESSORIOS = "#8c564b"
    PERFORMANCE = "#e377c2"
    NOSTALGIA = "#7f7f7f"
    LANCAMENTO = "#bcbd22"
    COMPARATIVO = "#17becf"
    PIRATARIA = "#aec7e8"
    SISTEMA_OPERACIONAL = "#ffbb78"
    EMULACAO = "#98df8a"
    HARDWARE_E_ESPECIFICACOES = "#ff9896"
    DESIGN_E_CONSTRUCAO = "#c5b0d5"
    RETROCOMPATIBILIDADE = "#c49c94"
    SERVICOS_ONLINE = "#f7b6d2"
    BATERIA = "#c7c7c7"
    MENSAGEM_PARA_O_YOUTUBER = "#dbdb8d"
    HUMOR_MEMES = "#9edae5"

    @classmethod
    def get_colors(cls):
        """Retorna todas as cores desse mapeamento"""
        return {category.name: category.value for category in cls}

COLOR_MAPPINGS = {
    "GAME_CONSOLE": GameConsoleCategoryColors.get_colors(),
    # "SMARTPHONE": SmartphoneCategoryColors.get_colors()
}