from flask import Flask, jsonify
import psycopg2
import redis
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        database='devops',
        user='ziad',
        password='secret123'
    )

def get_redis_connection():
    return redis.Redis(
        host=os.environ.get('REDIS_HOST', 'redis'),
        port=6379,
        decode_responses=True
    )

@app.route('/')
def hello():
    return jsonify({
        'service': 'ziad-devops-api',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.cursor().execute('SELECT 1')
        conn.close()
        return jsonify({'database': 'connected', 'status': 'healthy'})
    except Exception as e:
        return jsonify({'database': 'error', 'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/logs')
def logs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM logs ORDER BY created_at DESC LIMIT 5')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        'id': row[0],
        'message': row[1],
        'time': str(row[2])
    } for row in rows])

@app.route('/cache')
def cache_test():
    try:
        r = get_redis_connection()
        r.set('last_visit', 'Day 14: Redis is real')
        value = r.get('last_visit')
        return jsonify({
            'cache': 'connected',
            'value': value,
            'status': 'Redis caching works'
        })
    except Exception as e:
        return jsonify({'cache': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
