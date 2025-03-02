import uuid
import logging
from data_collector.youtube_collector import collect_youtube_data
from data_storage.data_inserter import insert_content_dataframe, insert_pipeline_log

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_collector(source, search, date_ranges, exec_id=None):
    exec_id = exec_id or uuid.uuid4()

    try:
        logging.info(f"🔎 Collecting data from {source} for {len(date_ranges)} date ranges with search term: {search}")

        df_comments = collect_youtube_data(search, date_ranges)

        if df_comments.empty:
            logging.warning("⚠️ No data collected.")
            insert_pipeline_log(exec_id, "Data Collection", "Warning", "No data collected.")
            return

        insert_content_dataframe(df_comments, source, exec_id)

        logging.info("✅ Collection and insertion completed successfully.")
        insert_pipeline_log(exec_id, "Data Collection", "Success", "Data collection completed successfully.")

    except Exception as e:
        error_message = f"❌ Error during data collection: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "Data Collection", "Error", error_message)
        raise  # 🔹 Propaga o erro para `run_pipeline()`
