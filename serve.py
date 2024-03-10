from flask import Flask, jsonify
import os

from waitress import serve

app = Flask(__name__)


# Endpoint to read and serve JSON data from outputs.json
@app.route("/miner-positions", methods=["GET"])
def get_cmw_data():
	output_json_path = os.path.abspath(os.path.join(path, "outputs/output.json"))
	if os.path.exists(output_json_path):
		with open(output_json_path, "r") as file:
			data = file.read()
		return jsonify(data)
	else:
		return f"{output_json_path} not found", 404


if __name__ == "__main__":
	path = "../prop-net/validation/"
	serve(app, host="0.0.0.0", port=80)
