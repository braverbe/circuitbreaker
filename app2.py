from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

failure_count = 0
last_failure_time = None
recovery_timeout = timedelta(seconds=10)


@app.route('/api')
def api():
    global failure_count, last_failure_time

    if last_failure_time is not None and datetime.now() - last_failure_time < recovery_timeout:
        return jsonify({'status': 'Service Unavailable'}), 503

    try:
        response = requests.get('http://127.0.0.1:5000/random')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException:
        failure_count += 1
        if failure_count >= 3:
            last_failure_time = datetime.now()
        return jsonify({'status': 'Service Unavailable'}), 503

if __name__ == '__main__':
    app.run(port=5001)
