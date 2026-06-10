from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        database='devops',
        user='ziad',
        password='secret123'
    )

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Ziad DevOps Day 10',
        'status': 'Kubernetes deployment successful'
    })

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
