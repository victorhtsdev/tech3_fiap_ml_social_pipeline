import os
import requests
import pandas as pd
from dotenv import load_dotenv
import logging

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
NUM_VIDEOS = int(os.getenv("YOUTUBE_NUM_VIDEOS", 4))  
NUM_VIDEOS_PER_REQUEST = int(os.getenv("YOUTUBE_NUM_VIDEOS_PER_REQUEST", 10))  
NUM_COMMENTS = int(os.getenv("YOUTUBE_NUM_COMMENTS", 2))
MAX_SEARCH_CALLS = int(os.getenv("YOUTUBE_MAX_SEARCH_CALLS", 5))
ALLOWED_COUNTRY = os.getenv("YOUTUBE_ALLOWED_COUNTRY", "BR")
ALLOWED_LANGUAGE = os.getenv("YOUTUBE_ALLOWED_LANGUAGE", "pt") 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_channel_info(channel_id):
    logging.info(f"🔍 Fetching channel information: {channel_id}")
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    channel_params = {
        "id": channel_id,
        "part": "snippet",
        "key": API_KEY
    }

    response = requests.get(channel_url, params=channel_params)
    
    if response.status_code != 200:
        logging.warning(f"⚠️ Failed to retrieve channel information {channel_id}: {response.json()}")
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
    logging.info(f"💬 Fetching comments for video {video_id}")
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
        logging.warning(f"⚠️ Failed to fetch comments for video {video_id}: {response.json()}")
        return {"items": []}

    return response.json()

def search_videos(search, start_date, end_date):
    logging.info(f"🔎 Searching videos for '{search}' between {start_date} and {end_date}")
    valid_videos = []
    next_page_token = None
    failed_attempts = 0
    search_calls = 0  

    try:
        while len(valid_videos) < NUM_VIDEOS and failed_attempts < MAX_SEARCH_CALLS:
            if search_calls >= MAX_SEARCH_CALLS:
                logging.warning(f"⚠️ Reached search call limit of {MAX_SEARCH_CALLS}.")
                break

            logging.info(f"📡 Calling YouTube API ({search_calls + 1}/{MAX_SEARCH_CALLS}) requesting {NUM_VIDEOS_PER_REQUEST} videos")
            search_url = "https://www.googleapis.com/youtube/v3/search"
            search_params = {
                "q": search,
                "type": "video",
                "part": "snippet",
                "order": "relevance",
                "regionCode": ALLOWED_COUNTRY,
                "relevanceLanguage": ALLOWED_LANGUAGE,
                "publishedAfter": f"{start_date}T00:00:00Z",
                "publishedBefore": f"{end_date}T23:59:59Z",
                "maxResults": NUM_VIDEOS_PER_REQUEST,
                "pageToken": next_page_token,
                "key": API_KEY
            }

            response = requests.get(search_url, params=search_params)
            search_calls += 1  

            if response.status_code != 200:
                logging.error(f"❌ YouTube API error ({response.status_code}): {response.json()}")
                raise Exception(f"YouTube API error ({response.status_code})")

            search_response = response.json()
            videos = search_response.get("items", [])

            logging.info(f"📌 Found {len(videos)} videos on page {search_calls}")

            if not videos:
                failed_attempts += 1
                continue

            for item in videos:
                if len(valid_videos) >= NUM_VIDEOS:
                    break 

                video_title = item["snippet"]["title"]
                video_id = item["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                channel_id = item["snippet"]["channelId"]
                video_date = item["snippet"]["publishedAt"]

                country, channel_title, channel_url = get_channel_info(channel_id)

                if country and country != ALLOWED_COUNTRY and ALLOWED_LANGUAGE not in video_title.lower():
                    logging.info(f"⏭️ Skipping video '{video_title}' ({video_id}) - Not allowed country or language")
                    continue

                logging.info(f"✅ Valid video found: {video_title} ({video_id})")

                valid_videos.append((video_title, video_id, video_url, channel_id, video_date, channel_title, channel_url))
                failed_attempts = 0  

            next_page_token = search_response.get("nextPageToken")
            if not next_page_token:
                break

    except Exception as e:
        logging.error(f"❌ Error in search_videos: {str(e)}")
        raise  

    return valid_videos

def collect_youtube_data(search, date_ranges):
    results = []
    logging.info(f"🚀 Starting data collection for '{search}'")

    try:
        for start_date, end_date in date_ranges:
            logging.info(f"📅 Collecting data for range {start_date} - {end_date}")
            videos = search_videos(search, start_date, end_date)

            if not videos:
                logging.info(f"⏭️ No videos found for range {start_date} - {end_date}")
                continue  

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
        logging.error(f"❌ Error in data collection: {str(e)}")
        raise  

    logging.info(f"🎯 Data collection completed. Total comments collected: {len(results)}")
    return pd.DataFrame(results)
