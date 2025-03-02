import os
import requests
import pandas as pd
from dotenv import load_dotenv
import logging

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

NUM_VIDEOS = int(os.getenv("YOUTUBE_NUM_VIDEOS", 4))
NUM_COMMENTS = int(os.getenv("YOUTUBE_NUM_COMMENTS", 2))

def get_channel_info(channel_id):
    """Obtém informações do canal pelo channel_id."""
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    channel_params = {
        "id": channel_id,
        "part": "snippet",
        "key": API_KEY
    }

    response = requests.get(channel_url, params=channel_params)

    if response.status_code != 200:
        logging.warning(f"⚠️ Falha ao obter informações do canal {channel_id}: {response.json()}")
        return None, None, None  

    channel_data = response.json()
    items = channel_data.get("items", [])

    if not items:
        return None, None, None

    snippet = items[0]["snippet"]
    country = snippet.get("country", "Unknown")  
    channel_title = snippet["title"]
    channel_url = f"https://www.youtube.com/channel/{channel_id}"

    return country, channel_title, channel_url

def fetch_comments(video_id):
    """Busca comentários de um vídeo do YouTube."""
    comments_url = "https://www.googleapis.com/youtube/v3/commentThreads"
    comments_params = {
        "videoId": video_id,
        "part": "snippet",
        "maxResults": NUM_COMMENTS,
        "order": "relevance",
        "key": API_KEY
    }

    response = requests.get(comments_url, params=comments_params)

    if response.status_code != 200:
        logging.warning(f"⚠️ Falha ao buscar comentários para vídeo {video_id}: {response.json()}")
        return {"items": []}

    return response.json()

def search_videos(search, start_date, end_date):
    valid_videos = []
    next_page_token = None

    try:
        while len(valid_videos) < NUM_VIDEOS:
            search_url = "https://www.googleapis.com/youtube/v3/search"
            search_params = {
                "q": search,
                "type": "video",
                "part": "snippet",
                "order": "relevance",
                "regionCode": "BR",
                "relevanceLanguage": "pt",
                "publishedAfter": f"{start_date}T00:00:00Z",
                "publishedBefore": f"{end_date}T23:59:59Z",
                "maxResults": NUM_VIDEOS,
                "pageToken": next_page_token,
                "key": API_KEY
            }

            response = requests.get(search_url, params=search_params)

            if response.status_code != 200:
                error_msg = f"❌ YouTube API error ({response.status_code}): {response.json()}"
                logging.error(error_msg)
                raise Exception(error_msg)

            search_response = response.json()
            videos = search_response.get("items", [])

            for item in videos:
                if len(valid_videos) >= NUM_VIDEOS:
                    break

                video_title = item["snippet"]["title"]
                video_id = item["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                channel_id = item["snippet"]["channelId"]
                video_date = item["snippet"]["publishedAt"]

                country, channel_title, channel_url = get_channel_info(channel_id)
                if country != "BR":
                    continue  

                valid_videos.append((video_title, video_id, video_url, channel_id, video_date, channel_title, channel_url))

            next_page_token = search_response.get("nextPageToken")
            if not next_page_token:
                break

    except Exception as e:
        logging.error(f"❌ Error in search_videos: {str(e)}")
        raise  

    return valid_videos

def collect_youtube_data(search, date_ranges):
    results = []

    try:
        for start_date, end_date in date_ranges:
            videos = search_videos(search, start_date, end_date)

            for video_title, video_id, video_url, channel_id, video_date, channel_title, channel_url in videos:
                comments = fetch_comments(video_id)

                for comment in comments.get("items", []):
                    comment_data = comment["snippet"]["topLevelComment"]["snippet"]
                    comment_text = comment_data["textDisplay"]
                    author = comment_data["authorDisplayName"]
                    comment_date = comment_data["publishedAt"]

                    results.append({
                        "video_title": video_title,
                        "video_id": video_id,
                        "video_url": video_url,
                        "video_date": video_date,
                        "channel_title": channel_title,
                        "channel_url": channel_url,
                        "author": author,
                        "comment_text": comment_text,
                        "comment_date": comment_date
                    })
                    
    except Exception as e:
        logging.error(f"❌ Error collecting YouTube data: {str(e)}")
        raise  

    return pd.DataFrame(results)
