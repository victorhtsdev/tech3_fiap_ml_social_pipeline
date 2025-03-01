import requests

API_KEY = "AIzaSyCTJFuTA_w2-4CLj58RzlMVzp2tZDHmgkY"  # Substitua pela sua chave de API
SEARCH_QUERY = "Nintendo Switch 2"

# 1️⃣ Buscar vídeos no YouTube
search_url = "https://www.googleapis.com/youtube/v3/search"
search_params = {
    "q": SEARCH_QUERY,
    "type": "video",
    "part": "snippet",
    "order": "relevance",
    "regionCode": "BR",  
    "relevanceLanguage": "pt",  
    "maxResults": 100,  
    "key": API_KEY
}

search_response = requests.get(search_url, params=search_params)
search_data = search_response.json()

# 2️⃣ Para cada vídeo, buscar detalhes do canal
for item in search_data.get("items", []):
    video_title = item["snippet"]["title"]
    video_id = item["id"]["videoId"]
    channel_id = item["snippet"]["channelId"]
    channel_title = item["snippet"]["channelTitle"]

    # 3️⃣ Buscar informações do canal
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    channel_params = {
        "id": channel_id,
        "part": "snippet",
        "key": API_KEY
    }

    channel_response = requests.get(channel_url, params=channel_params)
    channel_data = channel_response.json()

    # 4️⃣ Verificar o país do canal
    channel_info = channel_data.get("items", [])[0]["snippet"]
    country = channel_info.get("country", "Desconhecido")  # ⚠️ Nem sempre preenchido

    # 5️⃣ Filtrar apenas canais brasileiros 🇧🇷
    if country == "BR":
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"\n🎬 Canal: {channel_title} ({channel_id})")
        print(f"   🌎 País: {country}")
        print(f"   📌 Vídeo: {video_title}")
        print(f"   🔗 {video_url}")
        print("   💬 Comentários mais relevantes:")

        # 6️⃣ Buscar os 10 comentários mais relevantes do vídeo
        comments_url = "https://www.googleapis.com/youtube/v3/commentThreads"
        comments_params = {
            "videoId": video_id,
            "part": "snippet",
            "order": "relevance",  # 🔹 Mais relevantes primeiro
            "maxResults": 10,
            "key": API_KEY
        }

        comments_response = requests.get(comments_url, params=comments_params)
        comments_data = comments_response.json()

        # 7️⃣ Exibir os 10 comentários mais relevantes
        for i, comment in enumerate(comments_data.get("items", []), start=1):
            author = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            print(f"   💬 {i}. {author}: {text}\n")