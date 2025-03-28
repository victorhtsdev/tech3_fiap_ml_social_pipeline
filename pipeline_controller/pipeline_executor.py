import uuid 
from datetime import datetime
import logging
import asyncio
import calendar
from data_storage.data_inserter import insert_pipeline_log, insert_ml_execution
from data_collector.base_collector import run_collector
from data_processing.preprocessing import run_preprocessing
from data_processing.processing import process_content_data
from ml_classification.classification_service import run_classification
from embedding.embedding_generator import process_embeddings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_current_month_range():
    today = datetime.today()
    first_day = today.replace(day=1).strftime("%Y-%m-%d")
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1]).strftime("%Y-%m-%d")
    return [(first_day, last_day)]

def run_pipeline_stage(exec_id, search, stage, date_ranges=None):
    stages = ["data_collection", "content_preprocessing", "embedding_generation", "run_classification"]
    #stages = ["data_collection", "content_preprocessing","content_processing", "embedding_generation", "run_classification"]
    start_index = stages.index(stage)
    
    for current_stage in stages[start_index:]:
        try:
            if current_stage == "data_collection":
                insert_pipeline_log(exec_id, "Data Collection", "Started", f"Starting data collection for Exec ID: {exec_id}")
                run_collector("YouTube", search, date_ranges, exec_id)
                insert_pipeline_log(exec_id, "Data Collection", "Success", "Data collection completed successfully.")
            
            elif current_stage == "content_preprocessing": 
                insert_pipeline_log(exec_id, "Preprocessing Data", "Started", f"Starting preprocessing for Exec ID: {exec_id}")
                run_preprocessing(exec_id)  
                insert_pipeline_log(exec_id, "Preprocessing Data", "Success", "Preprocessing completed successfully.")

            elif current_stage == "embedding_generation":
                insert_pipeline_log(exec_id, "Embedding Generation", "Started", f"Starting embedding generation for Exec ID: {exec_id}")
                process_embeddings(exec_id)
                insert_pipeline_log(exec_id, "Embedding Generation", "Success", "Embedding generation completed successfully.")

            elif current_stage == "run_classification":
                insert_pipeline_log(exec_id, "ML Classification", "Started", f"Starting Classification for Exec ID: {exec_id}")
                run_classification(exec_id)
                insert_pipeline_log(exec_id, "ML Classification", "Success", "Classification completed successfully.")

        except Exception as e:
            logging.error(f"❌ {current_stage.replace('_', ' ').title()} failed: {str(e)}")
            insert_pipeline_log(exec_id, current_stage.replace('_', ' ').title(), "Error", f"{current_stage.replace('_', ' ').title()} failed for Exec ID: {exec_id}. Error: {str(e)}")
            return {"exec_id": str(exec_id), "status": "Failed"}
    
    return {"exec_id": str(exec_id), "status": "Success"}

async def run_pipeline(exec_id, search, date_ranges=None, classification_model_version=None, classification_model_name=None, classification_model_type=None):
    execution_date = datetime.now()
    search = search.upper()
    
    if not date_ranges:  
        date_ranges = get_current_month_range()  

    try:
        insert_pipeline_log(exec_id, "Pipeline Execution", "Started", f"Pipeline execution started. Search: {search}, Exec ID: {exec_id}")

        insert_ml_execution(
            exec_id=exec_id,
            search=search,
            date=execution_date,
            classification_model_version=classification_model_version,
            classification_model_name=classification_model_name,
            classification_model_type=classification_model_type,
            date_ranges=date_ranges
        )

        if run_pipeline_stage(exec_id, search, "data_collection", date_ranges)["status"] == "Failed":
            return {
                "exec_id": str(exec_id),
                "execution_id": str(exec_id),
                "status": "Failed"
            }
        
        insert_pipeline_log(exec_id, "Pipeline Execution", "Completed", "Pipeline execution completed successfully.")

        return {
            "exec_id": str(exec_id),
            "execution_id": str(exec_id),
            "status": "Success"
        }
    
    except Exception as e:
        error_message = f"❌ Pipeline execution failed: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "Pipeline Execution", "Error", error_message)
        
        return {
            "exec_id": str(exec_id),
            "execution_id": str(exec_id),
            "status": "Failed"
        }
