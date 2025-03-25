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
        logging.error(f"Erro ao converter embedding: {e}")
        return None

def run_classification(exec_id):
    try:
        logging.info(f"🔎 Iniciando processo de classificação para exec_id: {exec_id}")

        content_data = get_content_processed_data(exec_id)

        if not content_data:
            logging.warning(f"⚠️ Nenhum dado encontrado para exec_id: {exec_id}")
            insert_pipeline_log(exec_id, "Classification", "Warning", "Nenhum dado processado encontrado.")
            return
        
        df_content_processed = pd.DataFrame(content_data)

        if "sentence" not in df_content_processed.columns or "embeddings" not in df_content_processed.columns:
            raise ValueError("🚨 Erro: Colunas 'sentence' ou 'embeddings' estão ausentes nos dados!")

        logging.info(f"📊 {len(df_content_processed)} registros carregados para classificação.")

        df_content_processed["embedding"] = df_content_processed["embeddings"].apply(convert_bytea_to_array)
        df_content_processed.dropna(subset=["embedding"], inplace=True)

        if df_content_processed.empty:
            logging.warning(f"⚠️ Nenhum embedding válido encontrado para classificação.")
            insert_pipeline_log(exec_id, "Classification", "Warning", "Nenhum embedding válido encontrado.")
            return

        X = np.vstack(df_content_processed["embedding"].values)

        logging.info(f"📥 Carregando modelo SVM e LabelEncoder...")
        svm_model = load_model()
        label_encoder = load_label_encoder()


        logging.info(f"🚀 Executando classificação...")
        y_pred = svm_model.predict(X)

        predicted_labels = label_encoder.inverse_transform(y_pred)

        df_content_processed["label"] = predicted_labels

        update_classification_results(df_content_processed[["exec_id", "content_id", "processed_id", "label"]])

        logging.info(f"✅ Classificação concluída com sucesso para exec_id: {exec_id}")
        insert_pipeline_log(exec_id, "Classification", "Success", "Classificação concluída com sucesso.")
    
    except Exception as e:
        error_message = f"❌ Erro durante a classificação: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "Classification", "Error", error_message)
        raise
