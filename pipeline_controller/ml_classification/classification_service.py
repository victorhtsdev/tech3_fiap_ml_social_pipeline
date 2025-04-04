import logging
import os
import numpy as np
import pandas as pd
from data_storage.data_getter import get_content_processed_data, get_model_info_from_execution
from data_storage.data_inserter import insert_pipeline_log
from data_storage.data_update import update_classification_results
from ml_classification.model_manager import load_model, load_label_encoder, load_pca

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
        
        df = pd.DataFrame(content_data)

        if "sentence" not in df.columns or "embeddings" not in df.columns:
            raise ValueError("🚨 Error: Columns 'sentence' or 'embeddings' are missing from the data!")

        logging.info(f"📊 {len(df)} records loaded for classification.")

        df["embedding"] = df["embeddings"].apply(convert_bytea_to_array)
        df.dropna(subset=["embedding"], inplace=True)

        if df.empty:
            logging.warning("⚠️ No valid embeddings found for classification.")
            insert_pipeline_log(exec_id, "Classification", "Warning", "No valid embeddings found.")
            return

        X = np.vstack(df["embedding"].values)

        model_info = get_model_info_from_execution(exec_id)
        if not model_info:
            raise ValueError("❌ Could not retrieve model info from execution.")

        model_name = model_info["model_name"]
        model_type = model_info["model_type"]
        model_version = model_info["model_version"]

        if not model_name or not model_type or not model_version:
            raise ValueError("❌ Model metadata (name/type/version) is incomplete.")

        model_name_lower = model_name.lower()
        model_type_lower = model_type.lower()
        version_str = f"v{model_version}"

        model_file = f"{model_name_lower}_model_{model_type_lower}_{version_str}.pkl"
        label_file = f"{model_name_lower}_label_encoder_{model_type_lower}_{version_str}.pkl"
        pca_file = f"pca_{model_type_lower}_{version_str}.pkl"

        logging.info(f"📥 Loading model from {model_file} and label encoder from {label_file}...")

        model = load_model(model_file)
        label_encoder = load_label_encoder(label_file)

        try:
            pca = load_pca(pca_file)
            X = pca.transform(X)
            logging.info(f"📦 PCA successfully applied using {pca_file}")
        except FileNotFoundError:
            logging.info("ℹ️ PCA not found. Using raw embeddings.")

        model_name_upper = model_name.upper()
        logging.info(f"🚀 Running classification using {model_name_upper}...")

        y_pred = model.predict(X)

        predicted_labels = label_encoder.inverse_transform(y_pred)

        df["label"] = predicted_labels

        update_classification_results(df[["exec_id", "content_id", "processed_id", "label"]])

        logging.info(f"✅ Classification successfully completed for exec_id: {exec_id}")
        insert_pipeline_log(exec_id, "ML Classification", "Success", "Classification successfully completed.")

    except Exception as e:
        error_message = f"❌ Error during classification: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "ML Classification", "Error", error_message)
        raise
