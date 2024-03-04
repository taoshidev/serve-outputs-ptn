import hashlib
import json

from flask import Flask, jsonify
import os

from datetime import datetime, timezone

from waitress import serve

app = Flask(__name__)


# Endpoint to read and serve JSON data from cmw.json
@app.route("/cmw", methods=["GET"])
def get_cmw_data():
	cmw_json_path = os.path.abspath(os.path.join(path, "outputs/cmw.json"))
	if os.path.exists(cmw_json_path):
		with open(cmw_json_path, "r") as file:
			data = file.read()
		return jsonify(data)
	else:
		return f"{cmw_json_path} not found", 404


# Endpoint to read and serve JSON data from latest_predictions.json
@app.route("/predictions", methods=["GET"])
def get_predictions_data():
	predictions_json_path = os.path.abspath(
		os.path.join(path, "outputs/latest_predictions.json")
	)
	if os.path.exists(predictions_json_path):
		with open(predictions_json_path, "r") as file:
			data = file.read()
		return jsonify(data)
	else:
		return f"{predictions_json_path} not found", 404


@app.route("/weights", methods=["GET"])
def get_weights_data():
	predictions_json_path = os.path.abspath(
		os.path.join(path, "weights/valiweights.json")
	)
	if os.path.exists(predictions_json_path):
		with open(predictions_json_path, "r") as file:
			data = file.read()
		return jsonify(data)
	else:
		return f"{predictions_json_path} not found", 404


@app.route("/unique-predictions", methods=["GET"])
def get_unique_predictions_data():
	predictions_json_path = os.path.abspath(
		os.path.join(path, "outputs/latest_predictions.json")
	)
	results = {}
	if os.path.exists(predictions_json_path):
		with open(predictions_json_path, "r") as file:
			results = json.loads(file.read())

	predictions = []
	preds_to_miners = {}

	ts_list = []
	start_ms = results["BTCUSD-5m"][0]["start"]

	ts_list.append(start_ms)

	for i in range(1, 100):
		ts_list.append(start_ms + i * 60000 * 5)

	for ts in ts_list:
		print(datetime.utcfromtimestamp(ts / 1000).replace(tzinfo=timezone.utc))

	for v in results["BTCUSD-5m"]:
		hashed_preds = hashlib.sha256(str(v["predictions"]).encode()).hexdigest()
		if hashed_preds not in predictions:
			predictions.append(hashed_preds)
			preds_to_miners[v["miner_uid"]] = v["predictions"]

	return_results_dict = {i: {"timestamp": ts_list[i]} for i in range(0, 100)}

	for key, value in preds_to_miners.items():
		for i, v in enumerate(value):
			return_results_dict[i][key] = v

	return jsonify({"unique_predictions": [return_results_dict[i] for i in range(0, 100)]})


if __name__ == "__main__":
	path = "time-series-prediction-subnet/validation/"
	serve(app, host="0.0.0.0", port=80)
