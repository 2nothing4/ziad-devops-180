from flask import Flask, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"\n{'='*60}")
    print(f"ALERT RECEIVED at {datetime.now()}")
    print(f"{'='*60}")
    for alert in data.get('alerts', []):
        status = alert.get('status', 'unknown')
        name = alert.get('labels', {}).get('alertname', 'unknown')
        severity = alert.get('labels', {}).get('severity', 'unknown')
        summary = alert.get('annotations', {}).get('summary', 'no summary')
        print(f"\nStatus: {status.upper()}")
        print(f"Alert: {name}")
        print(f"Severity: {severity}")
        print(f"Summary: {summary}")
    print(f"{'='*60}\n")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
