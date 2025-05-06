from flask import Flask, request, jsonify
from blockchain_utils import BlockchainUtils
from anomaly_detection import AnomalyDetector
import os

app = Flask(__name__)

# Initialize blockchain and AI
blockchain = BlockchainUtils(os.getenv("ETH_NODE_URL"), os.getenv("CONTRACT_ADDRESS"))
ai_detector = AnomalyDetector(model_path="ai/model.h5")

@app.route("/add_record", methods=["POST"])
def add_record():
    data = request.json
    ipfs_hash = data["ipfs_hash"]
    patient_address = data["patient_address"]
    try:
        tx_hash = blockchain.add_record(ipfs_hash, patient_address)
        return jsonify({"status": "success", "tx_hash": tx_hash}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get_record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    address = request.args.get("address")
    try:
        record = blockchain.get_record(record_id, address)
        return jsonify({"status": "success", "record": record}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/analyze_data", methods=["POST"])
def analyze_data():
    data = request.json["patient_data"]  # Example: vitals, lab results
    try:
        anomaly_score = ai_detector.predict(data)
        return jsonify({"status": "success", "anomaly_score": anomaly_score}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)