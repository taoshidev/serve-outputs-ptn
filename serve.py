from flask import Flask, jsonify, request
import os
import requests
import json

from waitress import serve

app = Flask(__name__)

accessible_api_keys = [
	'xxxx'
]


def get_api_key():
	# Get the API key from the query parameters or request headers
	if "api_key" in request.json:
		api_key = request.json["api_key"]
	else:
		api_key = request.headers.get('Authorization')
		if api_key:
			api_key = api_key.split(' ')[1]  # Remove 'Bearer ' prefix
	return api_key


def get_file(f):
	output_json_path = os.path.abspath(os.path.join(path, f))
	if os.path.exists(output_json_path):
		with open(output_json_path, "r") as file:
			data = json.load(file)
		return data
	else:
		return None


# Endpoint to read and serve JSON data from outputs.json
@app.route("/miner-positions", methods=["GET"])
def get_miner_positions():
	api_key = get_api_key()

	# Check if the API key is valid
	if api_key not in accessible_api_keys:
		return jsonify({'error': 'Unauthorized access'}), 401
	else:
		print("api key received.")

	f = "outputs/output.json"
	data = get_file(f)

	if data is None:
		return f"{f} not found", 404
	else:
		return jsonify(data)


@app.route("/eliminations", methods=["GET"])
def get_eliminations():
	api_key = get_api_key()

	# Check if the API key is valid
	if api_key not in accessible_api_keys:
		return jsonify({'error': 'Unauthorized access'}), 401
	else:
		print("api key received.")

	f = "eliminations.json"
	data = get_file(f)

	if data is None:
		return f"{f} not found", 404
	else:
		return jsonify(data)


@app.route("/miner-copying", methods=["GET"])
def get_miner_copying():
	api_key = get_api_key()

	# Check if the API key is valid
	if api_key not in accessible_api_keys:
		return jsonify({'error': 'Unauthorized access'}), 401
	else:
		print("api key received.")

	f = "miner_copying.json"
	data = get_file(f)

	if data is None:
		return f"{f} not found", 404
	else:
		return jsonify(data)


if __name__ == "__main__":
	path = "proprietary-trading-network/validation/"
	serve(app, host="0.0.0.0", port=80)
