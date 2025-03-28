import logging
import numpy as np
import pandas as pd
from data_storage.data_getter import get_content_processed_data
from data_storage.data_inserter import insert_pipeline_log
from ml_classification.model_manager import load_model, load_label_encoder
from data_storage.data_update import update_classification_results

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def convert_bytea_to_array(bytea_data):
    if bytea_data is None:
        return None
    try:
        embedding = np.frombuffer(bytea_data, dtype=np.float32)
        return embedding if embedding.size > 0 else None
    except Exception as e:
        logging.error(f"Error converting embedding: {e}")
        return None

def run_classification(exec_id):
    try:
        logging.info(f"🔎 Starting classification process for exec_id: {exec_id}")

        content_data = get_content_processed_data(exec_id)

        if not content_data:
            logging.warning(f"⚠️ No data found for exec_id: {exec_id}")
            insert_pipeline_log(exec_id, "ML Classification", "Warning", "No processed data found.")
            return
        
        df_content_processed = pd.DataFrame(content_data)

        if "sentence" not in df_content_processed.columns or "embeddings" not in df_content_processed.columns:
            raise ValueError("🚨 Error: Columns 'sentence' or 'embeddings' are missing from the data!")

        logging.info(f"📊 {len(df_content_processed)} records loaded for classification.")

        df_content_processed["embedding"] = df_content_processed["embeddings"].apply(convert_bytea_to_array)
        df_content_processed.dropna(subset=["embedding"], inplace=True)

        if df_content_processed.empty:
            logging.warning(f"⚠️ No valid embeddings found for classification.")
            insert_pipeline_log(exec_id, "Classification", "Warning", "No valid embeddings found.")
            return

        X = np.vstack(df_content_processed["embedding"].values)

        logging.info(f"📥 Loading SVM model and LabelEncoder...")
        svm_model = load_model()
        label_encoder = load_label_encoder()

        logging.info(f"🚀 Running classification...")
        y_pred = svm_model.predict(X)

        predicted_labels = label_encoder.inverse_transform(y_pred)

        df_content_processed["label"] = predicted_labels

        update_classification_results(df_content_processed[["exec_id", "content_id", "processed_id", "label"]])

        logging.info(f"✅ Classification successfully completed for exec_id: {exec_id}")
        insert_pipeline_log(exec_id, "ML Classification", "Success", "Classification successfully completed.")
    
    except Exception as e:
        error_message = f"❌ Error during classification: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "ML Classification", "Error", error_message)
        raise
