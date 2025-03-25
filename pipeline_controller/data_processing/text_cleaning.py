import os
import logging
import nltk
from dotenv import load_dotenv
from nltk.corpus import stopwords
import re
import numpy as np
from nltk.tokenize import PunktSentenceTokenizer
import pandas as pd
import emoji
import string

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

from nltk.tokenize import PunktSentenceTokenizer

def split_comments_into_sentences(df, column='content'):
    processed_data = []
    
    sentence_tokenizer = PunktSentenceTokenizer()
    
    for _, row in df.iterrows():
        text = row[column]
        sentences = sentence_tokenizer.tokenize(text)

        if not sentences:
            sentences = [text]

        for sentence in sentences:
            processed_data.append({'sentence': sentence.strip()})

    return pd.DataFrame(processed_data)



def remove_urls_mentions_html(text):
    text = re.sub(r'http\S+|www\S+', '', text)  
    text = re.sub(r'@\w+', '', text)  
    text = re.sub(r'<a\s+href[^>]*', '', text)  
    text = re.sub(r'<.*?>', '', text)  
    return text

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def normalize_text(text):

    if not isinstance(text, str):
        return text 
    
    text = text.lower().strip() 
    text = text.replace("quot", "")  
    
    return text

def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

def clean_for_word_cloud(text):
    if not isinstance(text, str):
        return ""

    text = remove_urls_mentions_html(text)
    text = remove_emojis(text)
    text = normalize_text(text)

    words = re.findall(r"\b\w+\b", text.lower())

    all_stopwords = stop_words  

    filtered_words = [word for word in words if word not in all_stopwords]
    return " ".join(filtered_words)