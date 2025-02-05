from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
REQUEST_COUNT = Counter('request_count', 'Total number of requests received')

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    return "Cloud Monitoring Dashboard Running!"

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

