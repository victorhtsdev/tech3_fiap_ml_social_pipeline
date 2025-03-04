import uuid
from datetime import datetime
import logging
import asyncio
import calendar
from data_storage.data_inserter import insert_pipeline_log, insert_ml_execution
from data_storage.data_getter import get_latest_version
from data_collector.base_collector import run_collector
from data_processing.processing import process_content_data
from clustering.clustering import clustering_pipeline
from embedding.embedding_generator import process_embeddings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_current_month_range():
    today = datetime.today()
    first_day = today.replace(day=1).strftime("%Y-%m-%d")
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1]).strftime("%Y-%m-%d")
    return [(first_day, last_day)]

def run_pipeline_stage(exec_id, search, stage):
    stages = ["data_collection", "content_processing", "embedding_generation", "clustering"]
    start_index = stages.index(stage)
    
    for current_stage in stages[start_index:]:
        try:
            if current_stage == "data_collection":
                insert_pipeline_log(exec_id, "Data Collection", "Started", f"Starting data collection for Exec ID: {exec_id}")
                run_collector("YouTube", search, get_current_month_range(), exec_id)
                insert_pipeline_log(exec_id, "Data Collection", "Success", "Data collection completed successfully.")
            elif current_stage == "content_processing":
                insert_pipeline_log(exec_id, "Content Processing", "Started", f"Starting content processing for Exec ID: {exec_id}")
                process_content_data(exec_id)
                insert_pipeline_log(exec_id, "Content Processing", "Success", "Content processing completed successfully.")
            elif current_stage == "embedding_generation":
                insert_pipeline_log(exec_id, "Embedding Generation", "Started", f"Starting embedding generation for Exec ID: {exec_id}")
                process_embeddings(exec_id)
                insert_pipeline_log(exec_id, "Embedding Generation", "Success", "Embedding generation completed successfully.")
            elif current_stage == "clustering":
                insert_pipeline_log(exec_id, "Clustering", "Started", f"Starting clustering for Exec ID: {exec_id}")
                clustering_pipeline(exec_id)
                insert_pipeline_log(exec_id, "Clustering", "Success", "Clustering completed successfully.")
        except Exception as e:
            logging.error(f"❌ {current_stage.replace('_', ' ').title()} failed: {str(e)}")
            insert_pipeline_log(exec_id, current_stage.replace('_', ' ').title(), "Error", f"{current_stage.replace('_', ' ').title()} failed for Exec ID: {exec_id}. Error: {str(e)}")
            return {"exec_id": str(exec_id), "status": "Failed"}
    
    return {"exec_id": str(exec_id), "status": "Success"}

async def run_pipeline(exec_id, search, date_ranges=None):
    execution_date = datetime.now()
    search = search.upper()
    
    if not date_ranges:  
        date_ranges = get_current_month_range()  

    latest_version = get_latest_version(search) + 1  

    try:
        insert_pipeline_log(exec_id, "Pipeline Execution", "Started", f"Pipeline execution started. Search: {search}, Exec ID: {exec_id}")
        insert_ml_execution(exec_id, search, execution_date, latest_version)
        
        if run_pipeline_stage(exec_id, search, "data_collection")["status"] == "Failed":
            return {"exec_id": str(exec_id), "execution_id": str(exec_id), "version": latest_version, "status": "Failed"}
        
        insert_pipeline_log(exec_id, "Pipeline Execution", "Completed", "Pipeline execution completed successfully.")
        
        return {"exec_id": str(exec_id), "execution_id": str(exec_id), "version": latest_version, "status": "Success"}
    
    except Exception as e:
        error_message = f"❌ Pipeline execution failed: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "Pipeline Execution", "Error", error_message)
        
        return {"exec_id": str(exec_id), "execution_id": str(exec_id), "version": latest_version, "status": "Failed"}