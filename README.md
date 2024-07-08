
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

## Available Endpoints

### All Miners Positions 

@app.route("/miner-positions", methods=["GET"])

This endpoint takes an optional parameter "tier" which can be one of the following values: ['0', '30', '50', '100']

If tier is not provided, the returned payload is a raw json file in this format:

```
{
    "5C5GANtAKokcPvJBGyLcFgY5fYuQaXC3MpVt75codZbLLZrZ": {
        "all_time_returns": 1.046956054826957,
        "n_positions": 15,
        "percentage_profitable": 0.8666666666666667,
        "positions": [
            {
                "average_entry_price": 0.59559,
                "close_ms": 1714156813363,
                "current_return": 1.0002165919508386,
                "initial_entry_price": 0.59559,
                "is_closed_position": true,
                "miner_hotkey": "5C5GANtAKokcPvJBGyLcFgY5fYuQaXC3MpVt75codZbLLZrZ",
                "net_leverage": 0.0,
                "open_ms": 1714139478990,
                "orders": [
                    {
                        "leverage": -0.1,
                        "order_type": "SHORT",
                        "order_uuid": "18ca3cdf-b785-4f88-90a9-d2c06e8653b1",
                        "price": 0.59559,
                        "price_sources": [],
                        "processed_ms": 1714139478990
                    },
                    {
                        "leverage": 0.0,
                        "order_type": "FLAT",
                        "order_uuid": "c902c428-fcfb-43ca-ab79-117c957dbbfa",
                        "price": 0.5943,
                        "price_sources": [],
                        "processed_ms": 1714156813363
                    }
                ],
                "position_type": "FLAT",
                "position_uuid": "1f3f427f-6cbe-497c-af11-2fbef2ca3c10",
                "return_at_close": 1.0002095904346948,
                "trade_pair": [
                    "NZDUSD",
                    "NZD/USD",
                    7e-05,
                    0.001,
                    500
                ]
            },
...
```
Hotkeys are mapped to a data dict. The data dict contains positions which contain orders.

If a tier is provided, the returned payload will be a gzipped json file of the above schema but with the following differences:

* tier 100: 100% of posiitons show realtime data. Equivalent to the "tierless" json file.
* tier 50: 50% of positions show relatime data, 50% of postiions are 24 hour lagged
* tier 30: 30% of positions show realtime data, 70% of positions are 24 hour lagged
* tier 0: 100% of positions are 24 hour lagged (equivalent to the Taoshi dashboard)

The tiers enable granularity of data freshness for different pricing tiers when selling data. It also enables a less bandwidth-intensive option for tranfering data thanks to gzip. 

### Single Miner Positions

 @app.route("/miner-positions/<minerid>", methods=["GET"])

 Similar to the above endpoint but only returns the data dict for the specified hotkey. The returned payload is a raw json file.

### Miner Hotkeys

@app.route("/miner-hotkeys", methods=["GET"])

Returns all the hotkeys as seen in the metagraph from the validator's perspective.

### All Miners Statistics 

@app.route("/statistics", methods=["GET"])

Returns the statistic relevant for scoring miners. These statistics are also consumed by the Taoshi dashboard for visualization purposes.

### Single Miner Statistics 

@app.route("/statistics/<minerid>/", methods=["GET"])

Returns the statistic relevant for scoring the specified miner.

### Eliminations

@app.route("/eliminations", methods=["GET"])

Which miners are eliminated according to this validator. This is the same information visualized on the Taoshi dashboard.

Schema:

```
 "eliminations": [
    {
      "dd": 0.8977225405136061,
      "elimination_initiated_time_ms": 1711184954891,
      "hotkey": "5Dk2u35LRYEi9SC5cWamtzRkdXJJDLES7gABuey6cJ6t1ajK",
      "reason": "MAX_TOTAL_DRAWDOWN"
    },
    {
      "dd": 0.890604775902768,
      "elimination_initiated_time_ms": 1711204151504,
      "hotkey": "5G1iDH2gvdAyrpUD4QfZXATvGEtstRBiXWieRDeaDPRfPEcU",
      "reason": "MAX_TOTAL_DRAWDOWN"
    },
    {
```

### Miner Copying

@app.route("/miner-copying", methods=["GET"])

Automatically-generated plagairsm scores per miner. Coming soon


### Validator Checkpoint 

@app.route("/validator-checkpoint", methods=["GET"])

Everything required for a validator to restore it's state when starting for the first time. This includes all miner positions as well as derived data such as perf ledgers, challenge period data, and eliminations. 

Perf ledger schema:

```bash
"perf_ledgers": {
    "5C5GANtAKokcPvJBGyLcFgY5fYuQaXC3MpVt75codZbLLZrZ": {
      "cps": [
        {
          "accum_ms": 21600000,
          "gain": 0.12586433994869853,
          "last_update_ms": 1714161050595,
          "loss": -0.12587360888356938,
          "n_updates": 17213,
          "open_ms": 21599768,
          "prev_portfolio_ret": 0.9999907311080851
        },
        {
          "accum_ms": 21600000,
          "gain": 0.017040557887505504,
          "last_update_ms": 1714182650595,
          "loss": -0.016984326534111933,
          "n_updates": 2219,
          "open_ms": 21599768,
          "prev_portfolio_ret": 1.0000469635212756
        },
        {
...
```
Perf ledgers are built based off realtime price data and are consumed in the scoring logic. More info in the PTN repo.

## Usage with curl
Example `curl` commands to interact with the Flask server. Replace `<server_ip>` with your validator's IP address and `xxxx` with your API key that you hardcode in `serve.py`

### Get All Miner Positions
```bash
curl -X GET http://<server_ip>:48888/miner-positions -H "Content-Type: application/json" -d '{"api_key": "xxxx"}' -o miner_positions.json
```

### Get All Miner Positions as a gz with a specified tier
```bash
curl -X GET 'http://<server_ip>:48888/miner-positions?tier=0' -H "Content-Type: application/json" -d '{"api_key": "xxxx"}' -o miner_positions.json.gz
```

### Get Validator Checkpoint
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

