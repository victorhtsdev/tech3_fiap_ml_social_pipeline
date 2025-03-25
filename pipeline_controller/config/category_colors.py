CATEGORY_COLOR_MAPPINGS = {
    "GAME_CONSOLE": {
        "Vendas": "#1f77b4",
        "Jogos": "#ff7f0e",
        "Expectativa de compra": "#2ca02c",
        "Preço": "#d62728",
        "Rumores e Vazamentos": "#9467bd",
        "Periféricos e Acessórios": "#8c564b",
        "Performance": "#e377c2",
        "Nostalgia": "#7f7f7f",
        "Lançamento": "#bcbd22",
        "Comparativo": "#17becf",
        "Pirataria": "#aec7e8",
        "Sistema Operacional": "#ffbb78",
        "Emulação": "#98df8a",
        "Hardware e Especificações": "#ff9896",
        "Design e Construção": "#c5b0d5",
        "Retrocompatibilidade": "#c49c94",
        "Serviços Online": "#f7b6d2",
        "Bateria": "#c7c7c7",
        "Mensagem para o YouTuber": "#dbdb8d",
        "Humor/Memes": "#9edae5"
    }
}

def get_category_colors_list(model_type):
    return CATEGORY_COLOR_MAPPINGS.get(model_type.upper(), {})
