import os
import logging
import nltk
from dotenv import load_dotenv
from nltk.corpus import stopwords
from data_storage.data_getter import get_content_data
from data_storage.data_update import update_processed_content
from sqlalchemy.exc import SQLAlchemyError
import re

load_dotenv()

language = os.getenv("LANGUAGE", "en").lower()
if language == "pt":
    language = "portuguese"
else:
    language = "english"

nltk.download("stopwords")
stop_words = set(stopwords.words(language))

def preprocess_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = text.lower()
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

def process_content_data(exec_id):
    try:
        logging.info(f"🔄 Starting processing for exec_id: {exec_id}")

        content_records = get_content_data(exec_id)

        if not content_records:
            logging.warning(f"⚠️ No records found for exec_id: {exec_id}")
            return False

        processed_records = []
        for record in content_records:
            processed_content = preprocess_text(record["content"])
            record["content_processed"] = processed_content
            processed_records.append(record)

        update_processed_content(processed_records)

        logging.info(f"✅ Processing completed for exec_id: {exec_id}")
        return True

    except SQLAlchemyError as e:
        logging.error(f"❌ Database error: {str(e)}")
        raise

    except Exception as e:
        logging.error(f"❌ Unexpected error: {str(e)}")
        raise

def remove_urls_mentions_html(text):
    text = re.sub(r'http\S+|www\S+', '', text)  
    text = re.sub(r'@\w+', '', text)  
    text = re.sub(r'<a\s+href[^>]*', '', text)  
    text = re.sub(r'<.*?>', '', text)  
    return text
