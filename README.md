
# Flask API Server for PTN Outputs

## Overview
This Flask server is configured to serve the outputs of the [PTN repo (Bittensor subnet 8)](https://github.com/taoshidev/proprietary-trading-network/blob/main/docs/validator.md), which generates JSON files accessible via this API. The Flask code can easily be modified to serve outputs from any other Bittensor subnet.

## Security Warning
The API uses a simple token-based authentication system. The default API key is set to "xxxx". **Change this default API key before deploying in a production environment to prevent unauthorized access.**

## Configuration
### Changing the API Key
To enhance the security of your API, change the default API key in the `accessible_api_keys` list in `serve.py` to a more secure key.

### Making Server Accessible
By default, the server binds to `127.0.0.1` which only allows local requests. To allow access from any IP address, bind to `0.0.0.0`:
```python
serve(app, host="0.0.0.0", port=48888)
```

### Launching the server
On your validator, clone this repo in the same directory that the `proprietary-trading-network` repo is in, make desired edits, and then run
```bash
pm2 start serve.py --name serve
```

## Security Considerations
### Rate Limiting
Consider implementing rate limiting using out of the box Flask extensions like `Flask-Limiter` or custom implementations to prevent abuse and ensure fair use of the API.

### HTTPS
Deploy the Flask application over HTTPS in production to encrypt data in transit. This is typically done by placing the Flask application behind a reverse proxy that handles SSL/TLS termination.

### Firewall Configuration
Configure firewall rules to only allow traffic on necessary ports from trusted IP addresses.

## Usage with curl
Example `curl` commands to interact with the Flask server. Replace `<server_ip>` with your validator's IP address and `xxxx` with your API key that you hardcode in `serve.py`

### Get Miner Positions with curl
```bash
curl -X GET http://<server_ip>:48888/miner-positions -H "Content-Type: application/json" -d '{"api_key": "xxxx"}' -o miner_positions.json
```

### Get Validator Checkpoint with curl
```bash
curl -X GET http://<server_ip>:48888/validator-checkpoint -H "Content-Type: application/json" -d '{"api_key": "xxxx"}' -o validator_checkpoint.json
```

## Usage with Python
Example python code to interact with the Flask server.

### Get Validator Checkpoint with python

```python
import requests
import json

url = 'https://example.com/validator-checkpoint'
api_key = 'abcdefg'

data = {
'api_key': api_key
}
json_data = json.dumps(data)
headers = {
'Content-Type': 'application/json',
}
test = requests.get(url, data=json_data, headers=headers)
print(test)
with open('validator_checkpoint.json', 'w') as f:
    f.write(json.dumps(test.json()))
# print(json.loads(test.json()))

```


## Final Notes
This Flask server setup provides a simple template for serving API requests. If not using the Request Network, ensure all security measures are in place before deploying to a live environment. 

The Request Network is a Taoshi product which serves subnet data while handling security, rate limiting, data customization, and provide a polished customer-facing and validator setup UI.

