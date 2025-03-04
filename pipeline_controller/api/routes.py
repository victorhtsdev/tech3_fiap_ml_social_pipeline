import threading
import asyncio  
from flask import Blueprint, request, jsonify
import uuid
from pipeline_executor import run_pipeline

api = Blueprint("api", __name__)

@api.route("/run_pipeline", methods=["POST"])
def run_pipeline_api():
    data = request.json
    search = data.get("search", "Nintendo Switch 2")
    date_ranges = data.get("date_ranges", [])

    exec_id = uuid.uuid4()

    thread = threading.Thread(target=lambda: asyncio.run(run_pipeline(exec_id, search, date_ranges)))
    thread.start()

    return jsonify({"message": "Pipeline started", "exec_id": str(exec_id)})
