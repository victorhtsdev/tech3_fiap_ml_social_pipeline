import threading
import asyncio  
from flask import Blueprint, request, jsonify
import uuid
from pipeline_executor import run_pipeline
from data_storage.data_getter import get_latest_ml_execution
from data_storage.data_getter import get_pipeline_status
from data_storage.data_getter import get_ml_executions_by_search
from data_storage.data_getter import get_embeddings_by_exec_id
from data_storage.data_getter import get_svm_category_counts
from data_storage.data_getter import get_word_cloud_data
from data_storage.data_getter import get_category_colors
from data_storage.data_getter import get_content_highlight
from data_storage.data_getter import get_models_info
from .auth import token_required, generate_token
from data_storage.data_delete import delete_execution_data
from data_storage.data_getter import get_model_metrics_grouped
from data_storage.data_getter import get_sentences_by_label_grouped
from data_storage.data_getter import get_time_series_label_count

api = Blueprint("api", __name__)

@api.route("/run_pipeline", methods=["POST"])
@token_required
def run_pipeline_api():
    data = request.json
    search = data.get("search", "Nintendo Switch 2")
    date_ranges = data.get("date_ranges", [])

    classification_model_version = data.get("classification_model_version")  
    classification_model_name = data.get("classification_model_name")  
    classification_model_type = data.get("classification_model_type") 

    exec_id = uuid.uuid4()

    thread = threading.Thread(target=lambda: asyncio.run(
        run_pipeline(exec_id, search, date_ranges, classification_model_version, classification_model_name, classification_model_type)
    ))
    thread.start()

    return jsonify({"message": "Pipeline started", "exec_id": str(exec_id)})

@api.route("/get_ml_execution_last_version", methods=["GET"])
@token_required
def get_ml_execution_api():
    try:
        result = get_latest_ml_execution()

        if not result:
            return jsonify({"message": "No execution data found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@api.route("/get_pipeline_status", methods=["GET"])
@token_required
def get_pipeline_status_api():
    exec_id = request.args.get("exec_id")

    if not exec_id:
        return jsonify({"error": "Missing exec_id parameter"}), 400

    result = get_pipeline_status(exec_id)

    return jsonify(result)

@api.route("/get_ml_executions_by_search", methods=["GET"])
@token_required
def get_ml_executions_by_search_api():
    search = request.args.get("search")

    if not search:
        return jsonify({"error": "Missing search parameter"}), 400

    try:
        result = get_ml_executions_by_search(search)

        if not result:
            return jsonify({"message": "No execution data found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@api.route("/get_embeddings", methods=["GET"])
@token_required
def get_embeddings_api():
    exec_id = request.args.get("exec_id")

    if not exec_id:
        return jsonify({"error": "Missing exec_id parameter"}), 400

    try:
        result = get_embeddings_by_exec_id(exec_id)

        if not result:
            return jsonify({"message": "No embeddings found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@api.route("/get_svm_category_counts", methods=["GET"])
@token_required
def get_svm_category_counts_api():  
    exec_id = request.args.get("exec_id")

    if not exec_id:
        return jsonify({"error": "Missing exec_id parameter"}), 400

    try:
        data = get_svm_category_counts(exec_id) 

        if not data:
            return jsonify({"message": "No predictions found"}), 404

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@api.route("/get_word_cloud", methods=["GET"])
@token_required
def get_word_cloud():
    exec_id = request.args.get("exec_id")

    if not exec_id:
        return jsonify({"error": "Missing exec_id parameter"}), 400

    try:
        result = get_word_cloud_data(exec_id)

        if not result:
            return jsonify({"message": "No words found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@api.route("/get_category_colors", methods=["GET"])
@token_required
def get_category_colors_route():
    exec_id = request.args.get("exec_id", "").strip()

    if not exec_id:
        return jsonify({"error": "Parameter 'exec_id' is required"}), 400

    color_map = get_category_colors(exec_id)

    return jsonify(color_map)

@api.route("/get_content_highlight", methods=["GET"])
@token_required
def get_content_highlight_api():
    exec_id = request.args.get("exec_id", "").strip()
    content_id = request.args.get("content_id", "").strip()

    if not exec_id or not content_id:
        return jsonify({"error": "Parameters 'exec_id' and 'content_id' are required"}), 400

    try:
        result = get_content_highlight(exec_id, int(content_id))

        if "error" in result:
            return jsonify(result), result.get("status", 404)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@api.route("/get_models", methods=["GET"])
@token_required
def get_models_api():
    try:
        result = get_models_info()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@api.route("/get_token", methods=["GET"])
def get_token_api():
    return jsonify({"token": generate_token()})

@api.route("/delete_execution", methods=["DELETE"])
@token_required
def delete_execution_api():
    exec_id = request.args.get("exec_id", "").strip().strip('"')

    if not exec_id:
        return jsonify({"error": "Parameter 'exec_id' is required"}), 400

    try:
        delete_execution_data(exec_id)
        return jsonify({"message": f"Data successfully deleted for exec_id: {exec_id}"})

    except Exception as e:
        return jsonify({"error": f"Failed to delete data: {str(e)}"}), 500
    
@api.route("/get_model_metrics", methods=["GET"])
@token_required
def get_model_metrics_api():
    try:
        result = get_model_metrics_grouped()

        if not result:
            return jsonify({"message": "No model metrics found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@api.route("/get_sentences_by_label", methods=["GET"])
@token_required
def get_sentences_by_label_api():
    exec_id = request.args.get("exec_id", "").strip()
    label = request.args.get("label", "").strip()

    if not exec_id or not label:
        return jsonify({"error": "Parameters 'exec_id' and 'label' are required"}), 400

    try:
        result = get_sentences_by_label_grouped(exec_id, label)

        if not result:
            return jsonify({"message": "No sentences found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
    
@api.route("/get_time_series_label", methods=["GET"])
@token_required
def get_time_series_api():
    exec_id = request.args.get("exec_id", "").strip()

    if not exec_id:
        return jsonify({"error": "Parameter 'exec_id' is required"}), 400

    try:
        result = get_time_series_label_count(exec_id)

        if not result:
            return jsonify({"message": "No time series data found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500