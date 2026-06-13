from flask import Flask, jsonify, Response
import psycopg2
import redis
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        database='devops',
        user='ziad',
        password=os.environ.get('DB_PASSWORD', 'secret123')
    )

def get_redis_connection():
    return redis.Redis(
        host=os.environ.get('REDIS_HOST', 'redis'),
        port=6379,
        decode_responses=True
    )

@app.route('/')
def hello():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    start = time.time()
    result = jsonify({
        'service': 'ziad-devops-api',
        'status': 'running',
        'version': '1.0.0'
    })
    REQUEST_LATENCY.observe(time.time() - start)
    return result

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    start = time.time()
    try:
        conn = get_db_connection()
        conn.cursor().execute('SELECT 1')
        conn.close()
        result = jsonify({'database': 'connected', 'status': 'healthy'})
    except Exception as e:
        result = jsonify({'database': 'error', 'status': 'unhealthy', 'error': str(e)}), 500
    REQUEST_LATENCY.observe(time.time() - start)
    return result

@app.route('/logs')
def logs():
    REQUEST_COUNT.labels(method='GET', endpoint='/logs').inc()
    start = time.time()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM logs ORDER BY created_at DESC LIMIT 5')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = jsonify([{
        'id': row[0],
        'message': row[1],
        'time': str(row[2])
    } for row in rows])
    REQUEST_LATENCY.observe(time.time() - start)
    return result

@app.route('/cache')
def cache_test():
    REQUEST_COUNT.labels(method='GET', endpoint='/cache').inc()
    start = time.time()
    try:
        r = get_redis_connection()
        r.set('last_visit', 'Day 22: Metrics are real')
        value = r.get('last_visit')
        result = jsonify({
            'cache': 'connected',
            'value': value,
            'status': 'Redis caching works'
        })
    except Exception as e:
        result = jsonify({'cache': 'error', 'error': str(e)}), 500
    REQUEST_LATENCY.observe(time.time() - start)
    return result

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
