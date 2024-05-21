import sys

from flask import Flask, jsonify, request
import os
import time
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


def get_file(f, attempts=3):
    output_json_path = os.path.abspath(os.path.join(path, f))
    if not os.path.exists(output_json_path):
        return None

    for attempt_number in range(attempts):
        try:
            with open(output_json_path, "r") as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            if attempt_number == attempts - 1:
                print(f"serve.py Failed to decode JSON after multiple attempts: {e}")
                raise
            else:
                print(f"serve.py Attempt {attempt_number + 1} failed with JSONDecodeError, retrying...")
            time.sleep(1)  # Wait before retrying
        except Exception as e:
            print(f"serve.py Unexpected error reading file: {e}")
            raise

# Endpoint to read and serve JSON data from outputs.json
@app.route("/miner-positions", methods=["GET"])
def get_miner_positions():
    api_key = get_api_key()

    # Check if the API key is valid
    if api_key not in accessible_api_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

    f = "outputs/output.json"
    data = get_file(f)

    if data is None:
        return f"{f} not found", 404
    else:
        return jsonify(data)
    
@app.route("/miner-positions/<minerid>", methods=["GET"])
def get_miner_positions_unique(minerid):
    api_key = get_api_key()

    # Check if the API key is valid
    if api_key not in accessible_api_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

    f = "outputs/output.json"
    data = get_file(f)

    if data is None:
        return f"{f} not found", 404

    # Filter the data for the specified miner ID
    filtered_data = data.get(minerid, None)

    if filtered_data is None:
        return jsonify({'error': 'Miner ID not found'}), 404

    return jsonify(filtered_data)

# Endpoint to read and serve JSON data from outputs.json
@app.route("/miner-hotkeys", methods=["GET"])
def get_miner_hotkeys():
    api_key = get_api_key()

    # Check if the API key is valid
    if api_key not in accessible_api_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

    f = "outputs/output.json"
    data = get_file(f)

    if data is None:
        return f"{f} not found", 404

    miner_hotkeys = list(data.keys())

    if len(miner_hotkeys) == 0:
        return f"{f} not found", 404
    else:
        return jsonify(miner_hotkeys)

# serve miner positions v2 now named validator checkpoint
@app.route("/validator-checkpoint", methods=["GET"])
def get_validator_checkpoint():
    api_key = get_api_key()

    # Check if the API key is valid
    if api_key not in accessible_api_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

    f = "../runnable/validator_checkpoint.json"
    data = get_file(f)

    if data is None:
        return f"{f} not found", 404
    else:
        return jsonify(data)
    
# serve miner positions v2 now named validator checkpoint
@app.route("/statistics", methods=["GET"])
def get_validator_checkpoint_statistics():
    api_key = get_api_key()

    # Check if the API key is valid
    if api_key not in accessible_api_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

    f = "../runnable/minerstatistics.json"
    data = get_file(f)

    if data is None:
        return f"{f} not found", 404
    else:
        return jsonify(data)
    
# serve miner positions v2 now named validator checkpoint
@app.route("/statistics/<minerid>/", methods=["GET"])
def get_validator_checkpoint_statistics_unique(minerid):
    api_key = get_api_key()

    # Check if the API key is valid
    if api_key not in accessible_api_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

    f = "../runnable/minerstatistics.json"
    data = get_file(f)

    if data is None:
        return f"{f} not found", 404

    data_summary: list = data.get("data", None)
    for element in data_summary:
        if element.get("hotkey", None) == minerid:
            return jsonify(element)

    return jsonify({'error': 'Miner ID not found'}), 404


@app.route("/eliminations", methods=["GET"])
def get_eliminations():
    api_key = get_api_key()

    # Check if the API key is valid
    if api_key not in accessible_api_keys:
        return jsonify({'error': 'Unauthorized access'}), 401

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

    f = "miner_copying.json"
    data = get_file(f)

    if data is None:
        return f"{f} not found", 404
    else:
        return jsonify(data)


if __name__ == "__main__":
    # sys.argv[0] is the script name itself
    # Arguments start from sys.argv[1]
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "../proprietary-trading-network/validation/"
    print(path)
    serve(app, host="127.0.0.1", port=48888)
