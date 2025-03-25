import logging  
import pandas as pd
from data_storage.data_getter import get_content_data 
from data_storage.data_inserter import insert_pipeline_log, insert_content_processed
from data_processing.text_cleaning import (
    split_comments_into_sentences, 
    remove_urls_mentions_html,
    remove_emojis,
    normalize_text,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_preprocessing(exec_id): 
    try:
        logging.info(f"🔎 Starting preprocessing for exec_id: {exec_id}")

        content_data = get_content_data(exec_id)

        if not content_data:
            logging.warning(f"⚠️ No content found for exec_id: {exec_id}")
            insert_pipeline_log(exec_id, "Preprocessing", "Warning", "No content found.")
            return
        
        df_content = pd.DataFrame(content_data)

        if "content" not in df_content.columns:
            raise ValueError("🚨 Error: Missing 'content' column in data!")

        df_content["clean_content"] = (
            df_content["content"]
            .astype(str)  
            .apply(remove_urls_mentions_html)
            .apply(remove_emojis)
            .apply(normalize_text)
        )

        df_content["sentence"] = df_content["clean_content"].apply(
            lambda x: split_comments_into_sentences(pd.DataFrame({"clean_content": [x]}), column="clean_content")["sentence"].tolist()
            if isinstance(x, str) else []
        )

        df_content = df_content.explode("sentence", ignore_index=True)
        df_content.dropna(subset=["sentence"], inplace=True)

        df_sentences = df_content[["exec_id", "content_id", "sentence"]]
        df_sentences = df_sentences[df_sentences["sentence"].str.len() > 5]

        df_sentences["processed_id"] = df_sentences.groupby("content_id").cumcount() + 1

        insert_content_processed(df_sentences, exec_id)

        logging.info(f"✅ Preprocessing completed successfully for exec_id: {exec_id}")
        insert_pipeline_log(exec_id, "Preprocessing Data", "Success", "Preprocessing completed successfully.")
    
    except Exception as e:
        error_message = f"❌ Error during preprocessing: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "Preprocessing Data", "Error", error_message)
        raise
