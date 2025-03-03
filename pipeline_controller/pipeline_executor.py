import uuid
from datetime import datetime
import logging
import asyncio
import calendar
from data_storage.data_inserter import insert_pipeline_log, insert_ml_execution
from data_storage.data_getter import get_latest_version
from data_collector.base_collector import run_collector

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_current_month_range():
    today = datetime.today()
    first_day = today.replace(day=1).strftime("%Y-%m-%d")
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1]).strftime("%Y-%m-%d")
    return [(first_day, last_day)]

async def run_pipeline(exec_id, search, date_ranges=None):
    execution_date = datetime.now()

    if not date_ranges:  
        date_ranges = get_current_month_range()  

    latest_version = get_latest_version(search) + 1  

    try:
        insert_pipeline_log(exec_id, "Pipeline Execution", "Started", f"Pipeline execution started. Search: {search}, Exec ID: {exec_id}")

        insert_ml_execution(exec_id, search, execution_date, latest_version)

        insert_pipeline_log(exec_id, "Data Collection", "Started", f"Starting data collection. Execution ID: {exec_id} - Search: {search}")

        try:
            run_collector("YouTube", search, date_ranges, exec_id)  
        except Exception as e:
            logging.error(f"❌ Data collection failed: {str(e)}")
            insert_pipeline_log(exec_id, "Pipeline Execution", "Interrupted", "Pipeline execution interrupted due to data collection failure.")
            return {"exec_id": str(exec_id), "execution_id": str(exec_id), "version": latest_version, "status": "Failed"}

        insert_pipeline_log(exec_id, "Data Collection", "Success", "Data collection completed successfully.")
        insert_pipeline_log(exec_id, "Pipeline Execution", "Completed", "Pipeline execution completed successfully.")

        return {"exec_id": str(exec_id), "execution_id": str(exec_id), "version": latest_version, "status": "Success"}

    except Exception as e:
        error_message = f"❌ Pipeline execution failed: {str(e)}"
        logging.error(error_message)
        insert_pipeline_log(exec_id, "Pipeline Execution", "Error", error_message)

        return {"exec_id": str(exec_id), "execution_id": str(exec_id), "version": latest_version, "status": "Failed"}
